def test_ping_healthcheck(restful_booker_api):
    """Сервис отвечает на /ping."""
    response, _ = restful_booker_api.ping.ping(validate=False)

    assert response.status_code == 201