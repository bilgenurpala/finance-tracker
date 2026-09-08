from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: SecretStr
    ENVIRONMENT: Literal["development", "staging", "production"]
    ANTHROPIC_API_KEY: SecretStr | None = None
    DEBUG: bool = False

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_must_be_long(cls, v: SecretStr) -> SecretStr:
        if len(v.get_secret_value()) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def database_url_must_be_async(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL must use the postgresql+asyncpg:// driver")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
