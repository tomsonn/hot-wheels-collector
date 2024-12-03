from collections.abc import AsyncIterable
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient, ASGITransport

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from sqlalchemy.ext.asyncio import AsyncSession
from structlog.stdlib import BoundLogger
from structlog.stdlib import get_logger

from hot_wheels_collector.api import app
from hot_wheels_collector.database.engine import Database
from hot_wheels_collector.database.repository import HotWheelsRepository
from hot_wheels_collector.settings.base import Settings
from hot_wheels_collector.settings.database import TestingDatabaseSettings, DatabaseSettings


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


class TestDb(TestingDatabaseSettings):
    @property
    def dsn(self) -> PostgresDsn:
        return MultiHostUrl(f"{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}")


@pytest.fixture(scope="session")
def test_db() -> TestDb:
    return TestDb()


@pytest.fixture(scope="session")
async def settings(test_db: TestDb) -> Settings:
    return Settings(
        db=DatabaseSettings(
            db_dsn=test_db.dsn,
        )
    )


@pytest.fixture(scope="session")
async def session(settings: Settings) -> AsyncIterable[AsyncSession]:
    database = Database(settings)
    async with database.acquire() as session:
        yield session
    await database.aclose()


@pytest.fixture
async def database(session: AsyncSession) -> AsyncIterable[MagicMock]:
    async with session.begin_nested() as transaction:
        try:
            await transaction.start()
            mock_database = MagicMock(Database)
            mock_database.acquire.return_value.__aenter__.return_value = session
            yield mock_database
        finally:
            await transaction.rollback()


@pytest.fixture(scope="session")
async def logger() -> BoundLogger:
    return get_logger("hot-wheels-collector.test")


@pytest.fixture
async def hw_repository(database: Database, logger: BoundLogger) -> HotWheelsRepository:
    return HotWheelsRepository(
        db=database,
        logger=logger
    )


@pytest.fixture
async def client(  # noqa: PLR0913
    settings: Settings,
    database: Database,
    hw_repository: HotWheelsRepository,
    logger: BoundLogger
) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        app.dependency_overrides[Settings] = lambda: settings
        app.dependency_overrides[Database] = lambda: database
        app.dependency_overrides[HotWheelsRepository] = lambda: hw_repository
        app.dependency_overrides[BoundLogger] = lambda: logger

        yield client
