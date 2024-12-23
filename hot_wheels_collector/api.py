from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, Request

from starlette.responses import JSONResponse
from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.engine import Database
from hot_wheels_collector.database.repository import (
    HotWheelsRepository,
    HotWheelsRepositoryDependency,
)
from hot_wheels_collector.database.schemas import Models, Series
from hot_wheels_collector.deps import create_deps
from hot_wheels_collector.errors import GetSeriesQueryError
from hot_wheels_collector.models.api import FilteredSeriesResponse
from hot_wheels_collector.models.series import (
    SeriesBase,
    HWSeries,
)
from hot_wheels_collector.settings.base import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    dependencies = create_deps()
    database = dependencies.db

    app.dependency_overrides[Settings] = lambda: dependencies.settings
    app.dependency_overrides[Database] = lambda: database
    app.dependency_overrides[HotWheelsRepository] = lambda: dependencies.hw_repository
    app.dependency_overrides[BoundLogger] = lambda: dependencies.logger

    yield
    await database.aclose()


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
    model_id: str, repository: HotWheelsRepositoryDependency
) -> Models | JSONResponse:
    model = await repository.get_model(model_id)
    if not model:
        return JSONResponse({"error": "not_found"}, 404)

    return model


@app.exception_handler(GetSeriesQueryError)
def handle_get_series_query_error(
    _request: Request, exc: GetSeriesQueryError
) -> JSONResponse:
    return JSONResponse({"error": "invalid_query", "msg": str(exc)}, 400)


@app.get("/series/{series_id}", response_model=Series, tags=["Hot Wheels"])
async def get_series(
    series_id: str, repository: HotWheelsRepositoryDependency
) -> Series | JSONResponse:
    series = await repository.get_series_by_id(series_id)
    if not series:
        return JSONResponse({"error": "not_found"}, 404)

    return series


@app.get("/series", response_model=Series, tags=["Hot Wheels"])
async def filter_series(
    repository: HotWheelsRepositoryDependency,
    query: Annotated[SeriesBase, Depends()],
) -> FilteredSeriesResponse | JSONResponse:
    series = await repository.get_series_by_query(query)
    if not series:
        return JSONResponse({"error": "not_found"}, 404)

    return FilteredSeriesResponse(
        series=[HWSeries.model_validate(s.model_dump()) for s in series]
    )
