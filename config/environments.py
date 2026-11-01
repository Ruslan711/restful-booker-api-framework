from enum import StrEnum
from pathlib import Path

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Environment(StrEnum):
    DEV = "dev"
    STAGE = "stage"


_URLS: dict[Environment, str] = {
    Environment.DEV: "https://restful-booker.herokuapp.com",
    Environment.STAGE: "https://restful-booker.herokuapp.com",
}


class EnvironmentConfig(BaseSettings):
    booker_url: HttpUrl

    booker_username: str = Field(default="admin", validation_alias="BOOKER_USERNAME")
    booker_password: str = Field(default="password123", validation_alias="BOOKER_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


def load_environment(env: Environment) -> EnvironmentConfig:
    """Конфиг для выбранного окружения: URL из _URLS, креды из .env / переменных."""
    if env not in _URLS:
        raise ValueError(f"Неизвестное окружение: {env!r}")

    return EnvironmentConfig(booker_url=_URLS[env])
