import allure
import pytest

from utils.faker_data import generate_booking_payload
from models.booking import BookingRequest, BookingResponse
from models.auth import LoginRequest
from utils.helper import Helper


def _create_booking(booking_api) -> int:
    request = BookingRequest(**generate_booking_payload(with_additional=True))
    response = booking_api.create(request=request)
    Helper.attach_response(response)

    assert response.status_code == 200
    data = response.json()
    BookingResponse.model_validate(data)
    return data["bookingid"]


def _get_token(auth_api) -> str:
    request = LoginRequest(username="admin", password="password123")
    response = auth_api.login(request=request)
    Helper.attach_response(response)

    assert response.status_code == 200
    data = response.json()
    return data["token"]


@allure.feature("Booking")
@allure.title("Успешное создание бронирования со всеми полями")
def test_create_booking_full(booking_api):
    request = BookingRequest(**generate_booking_payload(with_additional=True))

    response = booking_api.create(request=request)
    Helper.attach_response(response)

    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@allure.feature("Booking")
@allure.title("Создание бронирования только с обязательными полями")
def test_create_booking_minimal(booking_api):
    request = BookingRequest(**generate_booking_payload(with_additional=False))

    response = booking_api.create(request=request)
    Helper.attach_response(response)

    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@allure.feature("Booking")
@allure.title("Создание бронирования с некорректными датами")
def test_create_booking_bad_dates(api_client):
    payload = generate_booking_payload(bad_dates=True)

    response = api_client.post("/booking", json=payload)
    Helper.attach_response(response)

    assert response.status_code == 200

    data = response.json()

    assert "bookingid" in data


@allure.feature("Booking")
@allure.title("Создание бронирования без обязательных полей")
def test_create_booking_without_required(api_client):
    response = api_client.post("/booking", json={})
    Helper.attach_response(response)

    assert response.status_code == 500


@allure.feature("Booking")
@allure.title("Получение бронирования по корректному ID")
def test_get_booking_by_id(booking_api):
    booking_id = _create_booking(booking_api)

    response = booking_api.get(booking_id)
    Helper.attach_response(response)

    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Получение бронирования по несуществующему ID")
def test_get_booking_not_found(booking_api):
    response = booking_api.get(booking_id=99999999)
    Helper.attach_response(response)

    assert response.status_code == 404


@allure.feature("Booking")
@allure.title("Получение списка всех бронирований")
def test_get_all_bookings(booking_api):
    response = booking_api.get_all()
    Helper.attach_response(response)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по имени")
@pytest.mark.parametrize("firstname", ["Jim", "Mary"])
def test_filter_by_firstname(booking_api, firstname):
    request = BookingRequest(
        firstname=firstname,
        lastname="TestLastname",
        totalprice=150,
        depositpaid=True,
        bookingdates={
            "checkin": "2026-01-01",
            "checkout": "2026-01-10",
        },
        additionalneeds="Breakfast",
    )

    created = booking_api.create(request=request)
    Helper.attach_response(created)

    assert created.status_code == 200

    created_id = created.json()["bookingid"]

    response = booking_api.get_all(firstname=firstname)
    Helper.attach_response(response)

    assert response.status_code == 200

    data = response.json()

    ids = [item["bookingid"] for item in data]

    assert created_id in ids


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по фамилии")
def test_filter_by_lastname(booking_api):
    request = BookingRequest(
        firstname="John",
        lastname="Smith",
        totalprice=120,
        depositpaid=True,
        bookingdates={
            "checkin": "2026-01-01",
            "checkout": "2026-01-05",
        },
        additionalneeds="Breakfast",
    )

    created = booking_api.create(request=request)
    Helper.attach_response(created)
    assert created.status_code == 200
    created_id = created.json()["bookingid"]

    response = booking_api.get_all(lastname="Smith")
    Helper.attach_response(response)
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    ids = [item["bookingid"] for item in data]
    assert created_id in ids


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по дате заезда")
@pytest.mark.parametrize(
    "checkin",
    ["2026-03-01", "2026-04-10"],
)
def test_filter_by_checkin(booking_api, checkin):
    response = booking_api.get_all(checkin=checkin)
    Helper.attach_response(response)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по дате выезда")
@pytest.mark.parametrize(
    "checkout",
    ["2026-06-01", "2026-07-15"],
)
def test_filter_by_checkout(booking_api, checkout):
    response = booking_api.get_all(checkout=checkout)
    Helper.attach_response(response)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


@allure.feature("Booking")
@allure.title("Полное успешное обновление бронирования (PUT)")
def test_update_booking_put(booking_api, auth_api):
    booking_id = _create_booking(booking_api)
    token = _get_token(auth_api)

    request = BookingRequest(**generate_booking_payload(with_additional=True))
    response = booking_api.update(booking_id, request=request, token=token)
    Helper.attach_response(response)

    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Частичное успешное обновление бронирования (PATCH)")
def test_update_booking_patch(booking_api, auth_api):
    booking_id = _create_booking(booking_api)
    token = _get_token(auth_api)

    base_request = BookingRequest(**generate_booking_payload(with_additional=True))
    patched_request = base_request.model_copy(update={"firstname": "UpdatedName"})

    response = booking_api.patch(booking_id, request=patched_request, token=token)
    Helper.attach_response(response)

    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Обновление бронирования без токена авторизации")
def test_update_without_token(api_client):
    booking_payload = generate_booking_payload(with_additional=True)

    response = api_client.put(
        "/booking/1",
        json=booking_payload,
    )

    Helper.attach_response(response)

    assert response.status_code == 403


@allure.feature("Booking")
@allure.title("Обновление бронирования с неверным токеном")
def test_update_wrong_token(api_client):
    headers = {
        "Cookie": "token=wrongtoken",
    }

    response = api_client.put(
        "/booking/1",
        json=generate_booking_payload(with_additional=True),
        headers=headers,
    )

    Helper.attach_response(response)

    assert response.status_code == 403


@allure.feature("Booking")
@allure.title("Обновление несуществующего бронирования")
def test_update_not_found(booking_api, auth_api):
    token = _get_token(auth_api)
    request = BookingRequest(**generate_booking_payload(with_additional=True))

    response = booking_api.update(
        booking_id=999999999,
        request=request,
        token=token,
    )
    Helper.attach_response(response)

    assert response.status_code == 405


@allure.feature("Booking")
@allure.title("Успешное удаление бронирования")
def test_delete_booking(booking_api, auth_api):
    booking_id = _create_booking(booking_api)
    token = _get_token(auth_api)

    response = booking_api.delete(
        booking_id,
        token=token,
    )

    Helper.attach_response(response)

    assert response.status_code == 201


@allure.feature("Booking")
@allure.title("Попытка удаления без токена авторизации")
def test_delete_without_token(api_client):
    response = api_client.delete("/booking/1")

    Helper.attach_response(response)

    assert response.status_code == 403


@allure.feature("Booking")
@allure.title("Удаление с неверным токеном авторизации")
def test_delete_wrong_token(api_client):
    headers = {
        "Cookie": "token=wrongtoken",
    }

    response = api_client.delete(
        "/booking/1",
        headers=headers,
    )

    Helper.attach_response(response)

    assert response.status_code == 403


@allure.feature("Booking")
@allure.title("Удаление несуществующего бронирования")
def test_delete_not_found(booking_api, auth_api):
    token = _get_token(auth_api)

    response = booking_api.delete(booking_id=346567344, token=token)
    Helper.attach_response(response)

    assert response.status_code == 405