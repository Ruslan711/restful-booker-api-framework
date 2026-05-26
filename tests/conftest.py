import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config.environments import Environment, EnvironmentConfig, load_environment


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