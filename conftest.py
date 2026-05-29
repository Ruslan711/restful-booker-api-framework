import pytest

from api.api_client import APIClient
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI
from config.environments import Environment, EnvironmentConfig, load_environment


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=Environment.DEV.value,
        choices=[env.value for env in Environment],
        help="Target environment for API tests",
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> Environment:
    """Выбранное окружение из опции --env."""
    env_value = request.config.getoption("--env")
    return Environment(env_value)


@pytest.fixture(scope="session")
def env_config(env: Environment) -> EnvironmentConfig:
    """Конфигурация выбранного окружения для всех тестов."""
    config = load_environment(env)

    print(f"\n[pytest] Running tests on environment: {env.value} ({config.booker_url})")

    return config


@pytest.fixture(scope="session")
def api_client(env_config: EnvironmentConfig) -> APIClient:
    """API клиент с URL из конфигурации окружения."""
    return APIClient(env_config.booker_url)


@pytest.fixture(scope="session")
def auth_api(api_client: APIClient) -> AuthAPI:
    return AuthAPI(api_client)


@pytest.fixture(scope="session")
def booking_api(api_client: APIClient) -> BookingAPI:
    return BookingAPI(api_client)
