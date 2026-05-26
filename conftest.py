import pytest

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
    env_value = request.config.getoption("--env")
    return Environment(env_value)


@pytest.fixture(scope="session")
def env_config(env: Environment) -> EnvironmentConfig:
    """Конфигурация выбранного окружения для всех тестов."""
    config = load_environment(env)

    print(f"\n[pytest] Running tests on environment: {env.value} ({config.booker_url})")

    return config