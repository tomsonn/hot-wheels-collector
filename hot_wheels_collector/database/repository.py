from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from hot_wheels_collector.database.engine import DatabaseDependency
from hot_wheels_collector.database.schemas import Models, Series
from hot_wheels_collector.errors import SeriesAlreadyExistsError
from hot_wheels_collector.models.models import HWModel
from hot_wheels_collector.models.series import SeriesBase, HWSeries
from hot_wheels_collector.settings.logger import LoggerDependency


class HotWheelsRepository:
    def __init__(self, db: DatabaseDependency, logger: LoggerDependency) -> None:
        self.__db = db
        self.__logger = logger

    # models
    async def get_model(self, model_id: str) -> Models | None:
        async with self.__db.acquire() as session:
            return (
                (await session.execute(select(Models).where(Models.id == model_id)))
                .scalars()
                .one_or_none()
            )

    async def create_model(self, model_scraped: HWModel, series: HWSeries) -> str:
        model_scraped_copy = model_scraped.model_copy()
        model_id = model_scraped_copy.compute_hash({"image_url"})
        if await self.get_model(model_id):
            self.__logger.warning(
                "create_model.model_already_exists", model_id=model_id
            )
            return model_id

        series_id = series.compute_hash({"description"})
        if not (_ := await self.get_series_by_id(series_id)):
            raise NoResultFound("create_model.series_not_found")

        model_db = Models(
            id=model_id, series_id=series_id, **model_scraped_copy.model_dump()
        )
        self.__logger.debug("create_model", model_id=model_id)
        async with self.__db.acquire(commit=True) as session:
            session.add(model_db)
            self.__logger.debug("model_created.success", model_id=model_db.id)
            return model_db.id

    # series
    async def get_series_by_id(self, series_id: str) -> Series | None:
        async with self.__db.acquire() as session:
            return (
                (await session.execute(select(Series).where(Series.id == series_id)))
                .scalars()
                .one_or_none()
            )

    async def get_series_by_query(self, series_request: SeriesBase) -> Sequence[Series]:
        statement = select(Series).where(Series.category == series_request.category)
        if series_request.name:
            statement = statement.where(Series.name == series_request.name)
        if series_request.release_year:
            statement = statement.where(
                Series.release_year == series_request.release_year
            )

        async with self.__db.acquire() as session:
            return (await session.execute(statement)).scalars().all()

    async def create_series(self, series: HWSeries) -> str:
        series_id = series.compute_hash({"description"})
        series_db = Series(**series.model_dump(), id=series_id)
        if await self.get_series_by_id(series_id):
            raise SeriesAlreadyExistsError("create_series.series_already_exists")

        async with self.__db.acquire(commit=True) as session:
            session.add(series_db)
            self.__logger.debug("series_created.success", series_id=series_db.id)
            return series_db.id


HotWheelsRepositoryDependency = Annotated[
    HotWheelsRepository, Depends(HotWheelsRepository)
]
