from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabasePoolConfig(BaseSettings):
    pool_size: int = 20
    max_overflow: int = 20
    pool_recycle: int = 600


class DatabaseSettings(BaseSettings):
    db_url: PostgresDsn
    pool_config: DatabasePoolConfig = DatabasePoolConfig()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class TestingDatabaseSettings(BaseSettings):
    scheme: Literal["postgresql"] = "postgresql"
    host: str = "localhost"
    user: str = "postgres"
    port: str = "5432"
    password: str = "postgres"
    name: str = "hw_collector_test"
    pool_config: DatabasePoolConfig = DatabasePoolConfig()

    model_config = SettingsConfigDict(
        env_prefix="test_db_",
        env_file=".env.test",
        env_file_encoding="utf-8",
        extra="ignore",
    )
