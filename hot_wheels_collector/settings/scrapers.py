from pathlib import Path
from typing import Any

from fake_useragent import UserAgent
from pydantic import BaseModel, HttpUrl


class HotWheelsModels(BaseModel):
    base_url: HttpUrl = HttpUrl("https://collecthw.com/find/years")
    hw_models_config_path: str = str(
        Path(__file__).parent.parent / "scrapers/config.yaml"
    )

    base_headers: dict[str, Any] = {
        "user-agent": UserAgent().chrome,
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip",
        "accept-language": "en-GB,en;q=0.9",
        "content-type": "text/html",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://collecthw.com/hw/year/1971",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    }
    base_referer: str = "https://collecthw.com/hw/year/"


class ScrapersConfig(BaseModel):
    hw_models: HotWheelsModels = HotWheelsModels()
