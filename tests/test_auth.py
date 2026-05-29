from services.restful_booker.auth.models.auth import AuthRequest


def test_auth_valid_credentials(restful_booker_api, test_data):
    creds = test_data["auth"]["valid"]
    payload = AuthRequest(**creds)

    response, model = restful_booker_api.auth.create_token(payload)

    assert response.status_code == 200
    assert model is not None
    assert model.token
