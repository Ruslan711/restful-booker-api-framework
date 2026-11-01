import pytest
import allure

from services.restful_booker.auth.assertions import (
    assert_auth_failed,
    assert_auth_successful,
)
from services.restful_booker.auth.models.auth import AuthRequest


@pytest.mark.smoke
@allure.title("Успешная авторизация с валидными кредами")
def test_auth_valid_credentials(api, env_config):
    creds = {
        "username": env_config.booker_username,
        "password": env_config.booker_password,
    }

    with allure.step("Собрать модель запроса авторизации"):
        payload = AuthRequest(**creds)

    with allure.step("Создание токена авторизации"):
        response, model = api.auth.create_token(payload)

    with allure.step("Проверить, что токен получен"):
        assert_auth_successful(response, model)


@pytest.mark.regression
@allure.title("Неуспешная авторизация: {case_name}")
@pytest.mark.parametrize(
    "case_name, username, password",
    [
        ("неверный пароль", None, "wrong-password"),
        ("неверный логин", "wrong-user", None),
    ],
)
def test_auth_invalid_credentials(api, env_config, test_data, case_name, username, password):
    expected_error = test_data["auth"]["expected_error"]

    invalid_creds = {
        "username": username or env_config.booker_username,
        "password": password or env_config.booker_password,
    }

    with allure.step("Собрать модель запроса с неверными данными"):
        payload = AuthRequest(**invalid_creds)

    with allure.step(f"Попытка авторизации: {case_name}"):
        response, _ = api.auth.create_token(payload, validate=False)

    with allure.step("Проверить, что авторизация не прошла"):
        assert_auth_failed(response, expected_error)
