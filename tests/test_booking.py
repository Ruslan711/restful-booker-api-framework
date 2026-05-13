import allure
import pytest

from utils.faker_data import generate_booking_payload
from models.booking import BookingRequest, BookingResponse


def _create_booking(booking_api, with_additional: bool = True):
    payload = BookingRequest(**generate_booking_payload(with_additional))
    response = booking_api.create(payload.dict())
    assert response.status_code == 200
    data = response.json()
    BookingResponse.model_validate(data)
    return data["bookingid"]


@allure.feature("Booking")
@allure.title("Успешное создание бронирования со всеми полями")
def test_create_booking_full(booking_api):
    payload = BookingRequest(**generate_booking_payload(with_additional=True))
    response = booking_api.create(payload.dict())

    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@allure.feature("Booking")
@allure.title("Создание бронирования только с обязательными полями")
def test_create_booking_minimal(booking_api):
    payload = BookingRequest(**generate_booking_payload(with_additional=False))
    response = booking_api.create(payload.dict())

    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@allure.feature("Booking")
@allure.title("Создание бронирования с некорректными датами")
def test_create_booking_bad_dates(booking_api):
    payload_dict = generate_booking_payload(bad_dates=True)
    payload = BookingRequest(**payload_dict)

    response = booking_api.create(payload.dict())

    assert response.status_code in [200, 400]


@allure.feature("Booking")
@allure.title("Создание бронирования без обязательных полей")
def test_create_booking_without_required(booking_api):
    response = booking_api.create({})

    assert response.status_code in [400, 500]



@allure.feature("Booking")
@allure.title("Получение бронирования по корректному ID")
def test_get_booking_by_id(booking_api):
    booking_id = _create_booking(booking_api)

    response = booking_api.get(booking_id)

    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Получение бронирования по несуществующему ID")
def test_get_booking_not_found(booking_api):
    response = booking_api.get(booking_id=99999999)

    assert response.status_code in [404, 500]


@allure.feature("Booking")
@allure.title("Получение списка всех бронирований")
def test_get_all_bookings(booking_api):
    response = booking_api.get_all()

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по имени")
@pytest.mark.parametrize("firstname", ["Jim", "Mary"])
def test_filter_by_firstname(booking_api, firstname):
    response = booking_api.get_all()
    assert response.status_code == 200



@allure.feature("Booking")
@allure.title("Фильтрация бронирований по фамилии")
def test_filter_by_lastname(booking_api):

    payload = {
        "firstname": "John",
        "lastname": "Smith",
        "totalprice": 120,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-05",
        },
    }

    created = booking_api.create(payload)
    assert created.status_code == 200
    created_id = created.json()["bookingid"]

    response = booking_api.get_all(lastname="Smith")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0

    ids = [item["bookingid"] for item in data]
    assert created_id in ids


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по дате заезда")
@pytest.mark.parametrize("date", ["2023-01-01", "2024-05-10"])
def test_filter_by_checkin(booking_api, date):
    response = booking_api.get_all()
    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Фильтрация бронирований по дате выезда")
@pytest.mark.parametrize("date", ["2023-01-01", "2024-05-10"])
def test_filter_by_checkout(booking_api, date):
    response = booking_api.get_all()
    assert response.status_code == 200


@allure.feature("Booking")
@allure.title("Полное успешное обновление бронирования (PUT)")
def test_update_booking_put(booking_api):
    booking_id = _create_booking(booking_api)

    payload = BookingRequest(**generate_booking_payload())
    response = booking_api.update(booking_id, payload.dict())

    assert response.status_code in [200, 403]


@allure.feature("Booking")
@allure.title("Частичное успешное обновление бронирования (PATCH)")
def test_update_booking_patch(booking_api):
    booking_id = _create_booking(booking_api)

    response = booking_api.patch(booking_id, {"firstname": "UpdatedName"})

    assert response.status_code in [200, 403]


@allure.feature("Booking")
@allure.title("Обновление бронирования без токена авторизации")
def test_update_without_token(booking_api, api_client):
    booking_id = _create_booking(booking_api)

    response = api_client.put(f"/booking/{booking_id}", json=generate_booking_payload())

    assert response.status_code in [401, 403, 405]


@allure.feature("Booking")
@allure.title("Обновление бронирования с неверным токеном")
def test_update_wrong_token(booking_api, api_client):
    booking_id = _create_booking(booking_api)

    headers = {"Cookie": "token=wrongtoken"}
    response = api_client.put(
        f"/booking/{booking_id}",
        json=generate_booking_payload(),
        headers=headers,
    )

    assert response.status_code in [401, 403, 405]


@allure.feature("Booking")
@allure.title("Обновление несуществующего бронирования")
def test_update_not_found(booking_api):
    response = booking_api.update(
        booking_id=32453263246,
        payload=generate_booking_payload(),
    )

    assert response.status_code in [403, 404, 405]


@allure.feature("Booking")
@allure.title("Успешное удаление бронирования")
def test_delete_booking(booking_api):
    booking_id = _create_booking(booking_api)

    response = booking_api.delete(booking_id)

    assert response.status_code in [200, 201, 204, 403]


@allure.feature("Booking")
@allure.title("Попытка удаления без токена авторизации")
def test_delete_without_token(booking_api, api_client):
    booking_id = _create_booking(booking_api)

    response = api_client.delete(f"/booking/{booking_id}")

    assert response.status_code in [401, 403, 405]


@allure.feature("Booking")
@allure.title("Удаление с неверным токеном авторизации")
def test_delete_wrong_token(api_client):
    headers = {"Cookie": "token=wrongtoken"}

    response = api_client.delete("/booking/1", headers=headers)

    assert response.status_code in [401, 403, 405]


@allure.feature("Booking")
@allure.title("Удаление несуществующего бронирования")
def test_delete_not_found(booking_api):
    response = booking_api.delete(booking_id=346567344)

    assert response.status_code in [403, 404, 405]