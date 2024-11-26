from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import asyncpg
from fastapi import Depends
from google.cloud.sql.connector import create_async_connector
from sqlalchemy.connectors import Connector
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from structlog.stdlib import get_logger

from hot_wheels_collector.settings.base import SettingsDependency
from hot_wheels_collector.settings.database import DatabaseSettings

logger = get_logger()

class Database:
    def __init__(self, settings: SettingsDependency) -> None:
        self.__settings = settings.db
        self.__connector: Connector | None = None
        self.__engine = self.create_engine(self.__settings)
        self.__session_maker = async_sessionmaker(self.__engine)

    def create_engine(self, settings: DatabaseSettings) -> AsyncEngine:
        async def getconn() -> asyncpg.Connection:
            conn: asyncpg.Connection = await asyncpg.connect(str(settings.db_dsn))
            return conn

        return create_async_engine("postgresql+asyncpg://", async_creator=getconn, **settings.pool_config.model_dump())

    async def __get_connector(self) -> Connector:
        if self.__connector is None:
            self.__connector = await create_async_connector()
        return self.__connector

    async def aclose(self) -> None:
        await self.__engine.dispose()

    @asynccontextmanager
    async def acquire(self, commit: bool = False) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_maker() as session:
            yield session
            if commit:
                await session.commit()


DatabaseDependency = Annotated[Database, Depends(Database)]
