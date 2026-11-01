import pytest
import allure
from utils.assertions import assert_status_code


@pytest.mark.smoke
@allure.title("Healthcheck /ping отвечает 201")
def test_ping_healthcheck(api):
    """Сервис отвечает на /ping."""
    with allure.step("Вызов /ping"):
        response, _ = api.ping.ping(validate=False)

    with allure.step("Проверить, что сервис ответил 201"):
        assert_status_code(response, 201)
