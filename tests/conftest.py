import json
import sys
import warnings
from pathlib import Path
from typing import Callable, Generator

import allure
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.environments import Environment, EnvironmentConfig, load_environment
from services.restful_booker.api import RestfulBookerApi
from services.restful_booker.auth.assertions import assert_auth_successful
from services.restful_booker.auth.models.auth import AuthRequest


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
    return load_environment(environment)


@pytest.fixture(scope="session")
def test_data(request: pytest.FixtureRequest) -> dict:
    """Тестовые данные по окружениям из test_data/{env}.json."""
    env_value = request.config.getoption("--env")
    environment = Environment(env_value)

    project_root = Path(__file__).parent.parent
    test_data_path = project_root / "test_data" / f"{environment.value}.json"

    with test_data_path.open(encoding="utf-8") as f:
        data = json.load(f)

    return data


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
    """Уборка ресурсов после теста."""
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
