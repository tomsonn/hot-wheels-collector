from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends
from pydantic import PositiveInt
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import select

from hot_wheels_collector.database.engine import DatabaseDependency
from hot_wheels_collector.database.schemas import Models, Series
from hot_wheels_collector.models.api import HotWheelsModelScraped, GetSeriesRequest
from hot_wheels_collector.settings.logger import LoggerDependency


class HotWheelsRepository:
    def __init__(self, db: DatabaseDependency, logger: LoggerDependency) -> None:
        self.__db = db
        self.__logger = logger

    async def get_model(self, model_id: PositiveInt) -> Models | None:
        async with self.__db.acquire() as session:
            return (await session.execute(select(Models).where(Models.id == model_id))).first()

    async def get_series(self, series_request: GetSeriesRequest) -> Series | None:
        statement = select(Series).where(Series.id == series_request.id if series_request.id else Series.name == series_request.name)
        async with self.__db.acquire() as session:
            try:
                res = (await session.execute(statement)).one()
                self.__logger.debug("get_series.success", series_id=res.id)
                return res
            except (MultipleResultsFound, NoResultFound) as e:
                self.__logger.error("get_series.failed", error=str(e), get_series_req=series_request.model_dump())
                return

    async def create_model(self, model_scraped: HotWheelsModelScraped) -> UUID | None:
        if not (series_id := await self.get_series(model_scraped.series_name)):
            return

        model_db = Models(**model_scraped.model_dump(exclude={"series_name"}), series_id=series_id)
        async with self.__db.acquire(commit=True) as session:
            await session.add(model_db)
            self.__logger.debug("model_created.success", model_id=model_db.id)
            return model_db.id


HotWheelsRepositoryDependency = Annotated[HotWheelsRepository, Depends(HotWheelsRepository)]
