import pytest
import allure

from models.auth import LoginRequest, LoginResponse, ErrorResponse
from utils.helper import Helper


@allure.feature("Auth")
@allure.title("Успешная авторизация с валидными данными")
def test_login_success(auth_api):
    request = LoginRequest(
        username="admin",
        password="password123",
    )

    response = auth_api.login(request=request)
    Helper.attach_response(response)

    assert response.status_code == 200

    data = response.json()
    LoginResponse.model_validate(data)

    assert "token" in data
    assert data["token"]


@allure.feature("Auth")
@allure.title("Негативные сценарии авторизации")
@pytest.mark.parametrize(
    "username,password,case,expected_status",
    [
        ("wrong", "wrong", "неверные учетные данные", 200),
        ("", "", "пустые учетные данные", 200),
        ("", "password123", "без имени пользователя", 200),
        ("admin", "", "без пароля", 200),
    ],
)
def test_login_negative(
    auth_api,
    username,
    password,
    case,
    expected_status,
):
    request = LoginRequest(
        username=username,
        password=password,
    )

    response = auth_api.login(request=request)
    Helper.attach_response(response)

    assert response.status_code == expected_status

    data = response.json()

    ErrorResponse.model_validate(data)

    assert data["reason"] == "Bad credentials"