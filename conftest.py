import pytest
from api.api_client import APIClient
from api.auth_api import AuthAPI
from api.booking_api import BookingAPI


BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL)


@pytest.fixture(scope="session")
def auth_api(api_client):
    return AuthAPI(api_client)


@pytest.fixture(scope="session")
def booking_api(api_client):
    return BookingAPI(api_client)