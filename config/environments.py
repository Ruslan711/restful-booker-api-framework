from enum import StrEnum

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEV = "dev"
    STAGE = "stage"


class EnvironmentConfig(BaseSettings):
    booker_url: HttpUrl

    booker_username: str = Field(validation_alias="BOOKER_USERNAME")
    booker_password: str = Field(validation_alias="BOOKER_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


_URLS: dict[Environment, str] = {
    Environment.DEV: "https://restful-booker.herokuapp.com",
    Environment.STAGE: "https://restful-booker.herokuapp.com",
}


def load_environment(env: Environment) -> EnvironmentConfig:
    return EnvironmentConfig(booker_url=_URLS[env])
