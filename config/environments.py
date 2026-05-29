import os
from enum import StrEnum
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(Path(__file__).parent.parent / ".env")


class Environment(StrEnum):
    DEV = "dev"
    STAGE = "stage"


class EnvironmentConfig(BaseSettings):
    booker_url: str
    booker_username: str
    booker_password: str

    model_config = SettingsConfigDict(
        env_prefix="BOOKER_",
    )


def load_environment(env: Environment) -> EnvironmentConfig:
    """Загружает конфигурацию из переменных окружения для указанного окружения."""
    if env not in (Environment.DEV, Environment.STAGE):
        raise ValueError(f"Неизвестное окружение: {env!r}")

    return EnvironmentConfig(
        booker_url=os.getenv("BOOKER_URL"),
        booker_username=os.getenv("BOOKER_USERNAME"),
        booker_password=os.getenv("BOOKER_PASSWORD"),
    )
