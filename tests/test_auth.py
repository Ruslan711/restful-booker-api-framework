import allure

from services.restful_booker.auth.assertions import (
    assert_auth_failed,
    assert_auth_successful,
)
from services.restful_booker.auth.models.auth import AuthRequest


@allure.title("Успешная авторизация с валидными кредами")
def test_auth_valid_credentials(api, test_data):
    creds = test_data["auth"]["valid"]
    payload = AuthRequest(**creds)

    with allure.step("Создание токена авторизации"):
        response, model = api.auth.create_token(payload)

    assert_auth_successful(response, model)


@allure.title("Неуспешная авторизация с неверными кредами")
def test_auth_invalid_credentials(api, test_data):
    valid_creds = test_data["auth"]["valid"]
    expected_error = test_data["auth"]["expected_error"]

    invalid_creds = {
        "username": valid_creds["username"],
        "password": valid_creds["password"] + "_wrong",
    }
    payload = AuthRequest(**invalid_creds)

    with allure.step("Попытка авторизации с неверными кредами"):
        response, _ = api.auth.create_token(payload, validate=False)

    assert_auth_failed(response, expected_error)
