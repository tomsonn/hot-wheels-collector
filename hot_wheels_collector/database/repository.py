from typing import Annotated

from fastapi import Depends
from pydantic import PositiveInt
from sqlmodel import select

from hot_wheels_collector.database.engine import DatabaseDependency
from hot_wheels_collector.database.models import Models
from hot_wheels_collector.settings.logger import LoggerDependency


class HotWheelsRepository:
    def __init__(self, db: DatabaseDependency, logger: LoggerDependency) -> None:
        self.__db = db
        self.__logger = logger

    async def get_model(self, model_id: PositiveInt) -> Models | None:
        async with self.__db.acquire() as session:
            return (await session.execute(select(Models).where(Models.id == model_id))).first()


HotWheelsRepositoryDependency = Annotated[HotWheelsRepository, Depends(HotWheelsRepository)]
