import time
from typing import Any, Literal

from requests import Response
from sqlalchemy.exc import NoResultFound
from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.repository import HotWheelsRepository
from hot_wheels_collector.errors import SeriesAlreadyExistsError
from hot_wheels_collector.helpers import load_yaml
from hot_wheels_collector.models.models import HWModel
from hot_wheels_collector.models.series import HWSeries
from hot_wheels_collector.scrapers.base import Scraper
from hot_wheels_collector.settings.base import Settings


class HotWheelsModels(Scraper):
    def __init__(
        self,
        hw_repository: HotWheelsRepository,
        logger: BoundLogger,
        settings: Settings,
    ) -> None:
        self.__config = load_yaml(settings.scrapers.hw_models.hw_models_config_path)
        self.__base_url = settings.scrapers.hw_models.base_url
        self.__headers = settings.scrapers.hw_models.base_headers
        self.__settings = settings

        super().__init__(hw_repository, logger)

    def _set_headers(self, headers: dict[str, Any], **kwargs) -> dict[str, Any]:
        if year := kwargs.get("year"):
            headers.update(
                {"referer": self.__settings.scrapers.hw_models.base_referer + str(year)}
            )
        self._session.headers.update(headers)

        return headers

    def _make_request(self, headers: dict[str, Any], *args, **kwargs) -> Response:
        self._set_headers(headers, **kwargs)
        return self._check_response_status(
            self._session.get, self.__base_url, params=self._get_query_params(**kwargs)
        )

    def _get_query_params(self, **kwargs) -> dict[str, Any]:
        if not (year := kwargs.get("year")):
            raise ValueError("Year is required to get query params")

        timestamp = int(time.time() * 1000)
        params = self.__config["hw_models"]["query_params"]
        params.update(
            {
                "query": year,
                "_": timestamp,
            }
        )
        if offset := kwargs.get("offset"):
            params.update({"start": offset})

        return params

    def _get_models_from_res(
        self, models_res: dict[str, Any], year: str
    ) -> list[tuple[HWModel, HWSeries]]:
        scraped_data = []
        total_records = models_res["recordsTotal"]
        filtered_records = models_res["recordsFiltered"]
        if total_records != filtered_records:
            self._logger.warning(
                "records_mismatch",
                total_records=total_records,
                filtered_records=filtered_records,
            )

        scraped_data.extend(
            [
                (self.__build_model(d), self.__build_series(d))
                for d in models_res["data"]
            ]
        )

        while offset := models_res["nextSkip"]:
            self._logger.info(
                "some_data_missing.continue_scraping", year=year, offset=offset
            )
            models_res = self._make_request(
                self.__headers, year=year, offset=offset
            ).json()

            scraped_data.extend(
                [
                    (self.__build_model(d), self.__build_series(d))
                    for d in models_res["data"]
                ]
            )

        return scraped_data

    @staticmethod
    def __build_model(response: dict[str, Any]) -> HWModel:
        return HWModel(
            name=response["ModelName"],
            collection_no=response["Col"],
            color=response["Color"],
            tampo=response["Tampo"],
            base_color=response["BaseColor"],
            base_type=response["BaseType"],
            window_color=response["WindowColor"]
            if response["WindowColor"] != "N\\A"
            else None,
            interior_color=response["InteriorColor"],
            wheel_type=response["WheelType"],
            toy_no=response["Toy"].split("-")[0],
            cast_no=response["Toy"].split("-")[-1] if "-" in response["Toy"] else None,
            toy_card=response["ToyCard"],
            scale=response["Scale"] or None,
            country=response["Country"],
            notes=response["Notes"],
            base_codes=response["BaseCodes"],
            sequence_no=response["SeriesNum"],
            release_year=int(response["Year"]),
            case_no=response["CaseNum"],
            assortment_no=response["AssortmentNum"],
            release_after=bool(response["ReleaseAfter"]),
            TH=bool(response["TH"]),
            STH=bool(response["STH"]),
            mainline=bool(response["Mainline"]),
            card_variant=bool(response["CardVariant"]),
            oversized_card=bool(response["OversizedCard"]),
        )

    @staticmethod
    def __build_series(response: dict[str, Any]) -> HWSeries:
        if not response["Mainline"] and not response["Series"]:
            category = "Unknown"
            name = None
        elif response["Mainline"]:
            category = "Mainline"
            name = response["Series"]
        else:
            category = response["Series"]
            name = None

        return HWSeries(
            category=category,
            name=name,
            release_year=int(response["Year"]),
        )

    async def __store_data(
        self,
        data_type: Literal["series", "models"],
        scraped_data: list[tuple[HWModel, HWSeries]],
    ) -> bool:
        store_model_error = False
        for data in scraped_data:
            try:
                if data_type == "series":
                    _ = await self._hw_repository.create_series(data[1])
                else:
                    _ = await self._hw_repository.create_model(*data)
            except (SeriesAlreadyExistsError, NoResultFound) as e:
                self._logger.error(f"create_{data_type}.error", error=e)
                if data_type == "models":
                    store_model_error = True

        return store_model_error

    async def __store_scraped_results(
        self, scraped_data: list[tuple[HWModel, HWSeries]]
    ) -> None:
        _ = await self.__store_data("series", scraped_data)
        store_model_error = await self.__store_data("models", scraped_data)

        # note(tm): not sure why, but sometimes happen, that the model is inserted earlier than a series, therefore, an exception (FK violation) is raised
        # my assumption is race condition, so let's try to store models once again
        if store_model_error:
            _ = await self.__store_data("models", scraped_data)

    async def run(self) -> None:
        # TODO - Once it will be running as a cronjob, let's compare the number of records in the DB with config - count of models by year.
        #  If the number of records differs than the config, then we need to scrape the data.
        for year, models_count in self.__config["hw_models"]["year"].items():
            self._logger.debug(
                "scraping_candidates", year=year, models_count=models_count
            )

            models_res = self._make_request(self.__headers, year=year).json()
            scraped_data = self._get_models_from_res(models_res, year)

            self._logger.debug("storing_data.started")
            await self.__store_scraped_results(scraped_data)
            self._logger.debug("storing_data.finished")

            self._logger.debug(
                "candidates_scraped.success", year=year, models_count=models_count
            )

        self._close_session()
