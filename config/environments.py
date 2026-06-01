from enum import StrEnum
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Доступные окружения для тестов."""
    DEV = "dev"
    STAGE = "stage"


class EnvironmentConfig(BaseSettings):
    """Конфигурация для API-тестов."""
    booker_url: str
    booker_username: Optional[str] = None
    booker_password: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="BOOKER_",
        env_file=".env",
        env_file_encoding="utf-8",
    )


_URLS: dict[Environment, str] = {
    Environment.DEV: "https://restful-booker.herokuapp.com",
    Environment.STAGE: "https://restful-booker.herokuapp.com",
}


def load_environment(env: Environment) -> EnvironmentConfig:
    """Загружает конфигурацию для выбранного окружения."""
    if env not in _URLS:
        raise ValueError(f"Неизвестное окружение: {env!r}")

    return EnvironmentConfig(booker_url=_URLS[env])
