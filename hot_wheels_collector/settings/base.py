from typing import Literal, Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings

from hot_wheels_collector.settings.database import DatabaseSettings


class Settings(BaseSettings):
    environment: Literal["production", "sandbox", "local", "test"]
    db: DatabaseSettings = DatabaseSettings()  # pyright: ignore


def get_settings() -> Settings:
    return Settings()


SettingsDependency = Annotated[Settings, Depends(get_settings)]
