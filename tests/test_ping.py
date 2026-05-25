import allure
from utils.assertions import assert_status_code


@allure.title("Healthcheck /ping отвечает 201")
def test_ping_healthcheck(api):
    """Сервис отвечает на /ping."""
    with allure.step("Вызов /ping"):
        response, _ = api.ping.ping(validate=False)

    assert_status_code(response, 201)