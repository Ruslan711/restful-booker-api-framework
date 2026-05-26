import allure


@allure.feature("Healthcheck")
@allure.title("API доступен")
def test_ping(api_client):
    response = api_client.get("/ping")

    assert response.status_code == 201