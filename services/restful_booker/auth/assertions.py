import allure
from requests import Response

from services.restful_booker.auth.models.auth import AuthResponse
from utils.assertions import assert_status_code


@allure.step("Проверка успешной авторизации")
def assert_auth_successful(response: Response, validated: AuthResponse | None) -> None:
    """Статус 200 и в ответе есть непустой токен."""
    assert_status_code(response, 200)

    assert validated is not None, "AuthResponse не должен быть None"
    assert validated.token, "Токен не должен быть пустым"


@allure.step("Проверка неуспешной авторизации")
def assert_auth_failed(response: Response, expected_error: str) -> None:
    """
    ВАЖНО: Restful Booker возвращает HTTP 200 даже при неверных credentials.
    Ошибка находится в поле reason тела ответа.
    """

    assert_status_code(response, 200)

    body = response.json()
    actual_reason = body.get("reason")

    assert actual_reason == expected_error, (
        f"Ожидали сообщение об ошибке '{expected_error}', но получили '{actual_reason}'"
    )
