import allure
from services.restful_booker.auth.models.auth import AuthRequest
from services.restful_booker.auth.assertions import assert_auth_successful


@allure.title("Успешная авторизация с валидными кредами")
def test_auth_valid_credentials(api, test_data):
    creds = test_data["auth"]["valid"]
    payload = AuthRequest(**creds)

    with allure.step("Создание токена авторизации"):
        response, model = api.auth.create_token(payload)

    assert_auth_successful(response, model)