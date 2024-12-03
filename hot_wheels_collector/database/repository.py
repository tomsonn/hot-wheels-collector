from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import select

from hot_wheels_collector.database.engine import DatabaseDependency
from hot_wheels_collector.database.schemas import Models, Series
from hot_wheels_collector.errors import SeriesAlreadyExistsError
from hot_wheels_collector.models.models import ScrapedHotWheelsModel
from hot_wheels_collector.models.series import CreateSeries, SeriesDetails
from hot_wheels_collector.settings.logger import LoggerDependency


class HotWheelsRepository:
    def __init__(self, db: DatabaseDependency, logger: LoggerDependency) -> None:
        self.__db = db
        self.__logger = logger

    # models
    async def get_model(self, model_id: UUID) -> Models | None:
        async with self.__db.acquire() as session:
            return (
                (await session.execute(select(Models).where(Models.id == model_id)))
                .scalars()
                .one_or_none()
            )

    async def create_model(self, model_scraped: ScrapedHotWheelsModel) -> UUID:
        if not (
            series := await self.get_series(
                SeriesDetails(name=model_scraped.series_name)
            )
        ):
            raise NoResultFound("create_model.series_not_found")

        model_db = Models(
            series_id=series.id,
            photo_url=str(model_scraped.photo_url),
            **model_scraped.model_dump(exclude={"series_name", "photo_url"}),
        )
        async with self.__db.acquire(commit=True) as session:
            session.add(model_db)
            self.__logger.debug("model_created.success", model_id=model_db.id)
            return model_db.id

    # series
    async def get_series(self, series_request: SeriesDetails) -> Series | None:
        statement = select(Series)
        if series_request.id:
            statement = statement.where(Series.id == series_request.id)
        if series_request.name:
            statement = statement.where(Series.name == series_request.name)
        if series_request.release_year:
            statement = statement.where(
                Series.release_year == series_request.release_year
            )

        self.__logger.info("series request", series_req=series_request)

        async with self.__db.acquire() as session:
            try:
                res = (await session.execute(statement)).scalars().one_or_none()
                self.__logger.debug(
                    "get_series.success", series_id=res.id if res else None
                )
                return res
            except MultipleResultsFound as e:
                self.__logger.error(
                    "get_series.failed",
                    error="Multiple series results were found",
                    get_series_req=series_request.model_dump(),
                )
                raise e

    # TODO - in case scraped model doesn't contain name of the series, create (or fetch) the default series, called "Unknown"
    async def create_series(self, series: CreateSeries) -> UUID:
        series_db = Series(**series.model_dump())
        get_series_req = SeriesDetails(
            name=series.name, release_year=series.release_year
        )
        if await self.get_series(get_series_req):
            raise SeriesAlreadyExistsError("create_series.series_already_exists")

        async with self.__db.acquire(commit=True) as session:
            session.add(series_db)
            self.__logger.debug("series_created.success", series_id=series_db.id)
            return series_db.id


HotWheelsRepositoryDependency = Annotated[
    HotWheelsRepository, Depends(HotWheelsRepository)
]
