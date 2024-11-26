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
