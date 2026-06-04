import pytest

from config.environments import (
    Environment,
    EnvironmentConfig,
    load_environment,
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=Environment.DEV.value,
        choices=[env.value for env in Environment],
    )


@pytest.fixture(scope="session")
def env_config(request: pytest.FixtureRequest) -> EnvironmentConfig:
    env_value = request.config.getoption("--env")
    environment = Environment(env_value)

    return load_environment(environment)
