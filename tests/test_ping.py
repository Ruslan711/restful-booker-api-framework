from utils.assertions import assert_status_code


def test_ping_healthcheck(restful_booker_api):
    """Сервис отвечает на /ping."""
    response, _ = restful_booker_api.ping.ping(validate=False)

    assert_status_code(response, 201)