import json
import warnings
from pathlib import Path
from typing import Callable, Generator

import allure
import pytest

from config.environments import Environment, EnvironmentConfig, load_environment
from services.restful_booker.api import RestfulBookerApi
from services.restful_booker.auth.assertions import assert_auth_successful
from services.restful_booker.auth.models.auth import AuthRequest

PROJECT_ROOT = Path(__file__).parent.parent


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=Environment.DEV.value,
        choices=[env.value for env in Environment],
        help="Окружение для запуска тестов",
    )


@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    env_value = request.config.getoption("--env")
    return load_environment(Environment(env_value))


@pytest.fixture(scope="session")
def test_data(request: pytest.FixtureRequest) -> dict:
    env_value = request.config.getoption("--env")
    environment = Environment(env_value)

    path = PROJECT_ROOT / "test_data" / f"{environment.value}.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def api(env_config: EnvironmentConfig) -> RestfulBookerApi:
    return RestfulBookerApi(env_config)


@pytest.fixture(scope="session")
def set_token(api: RestfulBookerApi, test_data: dict) -> str:
    creds = test_data["auth"]["valid"]
    payload = AuthRequest(**creds)

    with allure.step("Создание токена"):
        response, model = api.auth.create_token(payload)

    assert_auth_successful(response, model)
    return model.token


@pytest.fixture
def cleanup() -> Generator[list[Callable[[], None]], None, None]:
    tasks: list[Callable[[], None]] = []
    yield tasks

    errors: list[Exception] = []

    for task in reversed(tasks):
        try:
            task()
        except Exception as exc:
            errors.append(exc)

    if errors:
        warnings.warn(f"Cleanup errors: {errors}")
