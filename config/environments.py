from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEV = "dev"
    STAGE = "stage"


class EnvironmentConfig(BaseSettings):
    booker_url: str
    booker_username: str
    booker_password: str

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
    if env not in _URLS:
        raise ValueError(f"Неизвестное окружение: {env!r}")

    return EnvironmentConfig(booker_url=_URLS[env])