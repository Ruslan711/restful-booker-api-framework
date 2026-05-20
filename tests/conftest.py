import pytest

from config.environments import Environment, load_environment


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=Environment.DEV.value,
        choices=[Environment.DEV.value, Environment.STAGE.value],
        help="Target environment for API tests: dev or stage",
    )


@pytest.fixture(scope="session")
def env(request) -> Environment:
    value = request.config.getoption("--env")
    return Environment(value)


@pytest.fixture(scope="session")
def env_config(env: Environment):
    config = load_environment(env)
    print(f"\n[pytest] Running tests on environment: {env.value} ({config.booker_url})")
    return config