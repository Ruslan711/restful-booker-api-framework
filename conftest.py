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

PROJECT_ROOT = Path(__file__).parent


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
    """Конфигурация выбранного окружения для всех тестов."""
    env_value = request.config.getoption("--env")
    environment = Environment(env_value)
    config = load_environment(environment)
    print(f"\n[pytest] Running tests on environment: {environment.value} ({config.booker_url})")
    return config


@pytest.fixture(scope="session")
def test_data(request: pytest.FixtureRequest) -> dict:
    """Тестовые данные по окружениям из test_data/{env}.json."""
    env_value = request.config.getoption("--env")
    environment = Environment(env_value)

    test_data_path = PROJECT_ROOT / "test_data" / f"{environment.value}.json"

    with test_data_path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def api(env_config: EnvironmentConfig) -> RestfulBookerApi:
    """Фасад для работы с Restful Booker API."""
    return RestfulBookerApi(env_config)


@pytest.fixture(scope="session")
def set_token(api: RestfulBookerApi, test_data: dict) -> str:
    """Создаёт токен для авторизованных операций и возвращает его значение."""
    creds = test_data["auth"]["valid"]
    payload = AuthRequest(**creds)

    with allure.step("Создание токена авторизации для тестов"):
        response, model = api.auth.create_token(payload)

    assert_auth_successful(response, model)
    return model.token  # type: ignore[union-attr]


@pytest.fixture
def cleanup() -> Generator[list[Callable[[], None]], None, None]:
    """
    Универсальная фикстура cleanup:
    накопленные задачи выполняются после теста в обратном порядке.
    """
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
