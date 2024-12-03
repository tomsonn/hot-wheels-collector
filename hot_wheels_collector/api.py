from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, Depends, Request

from starlette.responses import JSONResponse
from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.engine import Database
from hot_wheels_collector.database.repository import (
    HotWheelsRepository,
    HotWheelsRepositoryDependency,
)
from hot_wheels_collector.database.schemas import Models, Series
from hot_wheels_collector.errors import GetSeriesQueryError
from hot_wheels_collector.models.series import SeriesDetails
from hot_wheels_collector.settings.base import Settings
from hot_wheels_collector.settings.logger import configure_logger, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()  # type: ignore
    logger = configure_logger()
    db = Database(settings)
    hw_repository = HotWheelsRepository(db, logger)

    app.dependency_overrides[Settings] = lambda: settings
    app.dependency_overrides[Database] = lambda: db
    app.dependency_overrides[HotWheelsRepository] = lambda: hw_repository
    app.dependency_overrides[BoundLogger] = lambda: logger

    yield
    await db.aclose()


app = FastAPI(
    title="Hot Wheels Collector API",
    openapi_url="/openapi.json",
    docs_url="/openapi",
    redoc_url="/docs",
    lifespan=lifespan,
)


@app.get("/ping")
def ping() -> dict:
    return {"ping": "pong"}


@app.get("/model/{model_id}", response_model=Models, tags=["Hot Wheels"])
async def get_model(
    model_id: UUID, repository: HotWheelsRepositoryDependency
) -> Models | JSONResponse:
    logger = get_logger()
    logger.info("model id in api", model_id=model_id)
    model = await repository.get_model(model_id)
    if not model:
        return JSONResponse({"error": "not_found"}, 404)

    return model


@app.exception_handler(GetSeriesQueryError)
def handle_get_series_query_error(
    _request: Request, exc: GetSeriesQueryError
) -> JSONResponse:
    return JSONResponse({"error": "invalid_query", "msg": str(exc)}, 400)


@app.get("/series", response_model=Series, tags=["Hot Wheels"])
async def get_series(
    repository: HotWheelsRepositoryDependency,
    query: Annotated[SeriesDetails, Depends()],
) -> Series | JSONResponse:
    series = await repository.get_series(query)
    if not series:
        return JSONResponse({"error": "not_found"}, 404)

    return series
