from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable

import requests
from requests import Response, HTTPError
from structlog.stdlib import BoundLogger

from hot_wheels_collector.database.repository import HotWheelsRepository


class PageType(str, Enum):
    home_page = "home_page"
    model_page = "model_page"
    series_page = "series_page"


class Scraper(ABC):
    def __init__(self, hw_repository: HotWheelsRepository, logger: BoundLogger) -> None:
        self._hw_repository = hw_repository
        self._logger = logger

        self._session = requests.Session()

    @abstractmethod
    def _set_headers(self, headers: dict[str, Any], **kwargs) -> dict[str, Any]: ...

    @abstractmethod
    def _make_request(self, headers: dict[str, Any], *args, **kwargs) -> Response: ...

    @abstractmethod
    async def run(self) -> None: ...

    def _close_session(self) -> None:
        self._session.close()

    def _check_response_status(self, func: Callable, *args, **kwargs) -> Response:
        response: Response = func(*args, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as e:
            self._logger.error("making_request.error", error=e)
            raise e
        return response
