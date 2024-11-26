from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.engine import Database
from hot_wheels_collector.settings.base import Settings
from hot_wheels_collector.settings.logger import configure_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    logger = configure_logger()
    db = Database(settings)

    app.dependency_overrides[Settings] = lambda: settings
    app.dependency_overrides[Database] = lambda: db
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
