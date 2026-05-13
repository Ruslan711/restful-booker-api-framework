import pytest
import allure

from models.auth import LoginRequest, LoginResponse, ErrorResponse


@allure.feature("Auth")
@allure.title("Успешная авторизация с валидными данными")
def test_login_success(auth_api):
    payload = LoginRequest(username="admin", password="password123")

    response = auth_api.login(**payload.dict())
    data = response.json()

    assert response.status_code == 200
    LoginResponse.model_validate(data)


@allure.feature("Auth")
@allure.title("Негативные сценарии авторизации")
@pytest.mark.parametrize(
    "username,password,case",
    [
        ("wrong", "wrong", "неверные учетные данные"),
        ("", "", "пустые учетные данные"),
        ("", "password123", "без имени пользователя"),
        ("admin", "", "без пароля"),
    ],
)
def test_login_negative(auth_api, username, password, case):
    response = auth_api.login(username=username, password=password)
    data = response.json()

    assert response.status_code in [200, 400]
    if "token" in data:
        assert not data["token"]
    if isinstance(data, dict) and "reason" in data:
        ErrorResponse.model_validate(data)