from typing import Literal, Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings

from hot_wheels_collector.settings.database import DatabaseSettings
from hot_wheels_collector.settings.scrapers import ScrapersConfig


class Settings(BaseSettings):
    environment: Literal["production", "sandbox", "local", "test"]
    db: DatabaseSettings = DatabaseSettings()  # pyright: ignore
    scrapers: ScrapersConfig = ScrapersConfig()


def get_settings() -> Settings:
    return Settings()  # type: ignore


def is_local_env() -> bool:
    return get_settings().environment in ["local", "test"]


SettingsDependency = Annotated[Settings, Depends(get_settings)]
