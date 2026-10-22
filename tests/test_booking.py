import pytest
from datetime import datetime, timedelta
from typing import Any

import allure
from faker import Faker

from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_booking_deleted,
    assert_booking_get,
    assert_booking_in_list,
    assert_booking_updated,
    assert_forbidden,
    assert_not_found,
)
from services.restful_booker.booking.models.booking import Booking

fake = Faker()


def _make_booking(with_additional: bool) -> Booking:
    checkin = datetime.now().date()
    checkout = checkin + timedelta(days=3)

    payload: dict[str, Any] = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=500),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": str(checkin),
            "checkout": str(checkout),
        },
    }

    if with_additional:
        payload["additionalneeds"] = fake.word()

    return Booking(**payload)


def _cleanup_booking(api, booking_id: int, token: str) -> None:
    delete_response, _ = api.booking.remove(
        booking_id,
        token=token,
    )
    assert_booking_deleted(delete_response)


@pytest.mark.regression
@allure.title("Создание брони со всеми полями")
def test_create_booking_all_params(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=True)

    with allure.step("Создание бронирования"):
        response, validated = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, validated.bookingid, set_token))

    with allure.step("Проверить, что бронь создана"):
        assert_booking_created(response, validated, new_booking)


@pytest.mark.smoke
@allure.title("Создание брони с минимальным набором полей")
def test_create_booking_minimal(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=False)

    with allure.step("Создание бронирования"):
        response, validated = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, validated.bookingid, set_token))

    with allure.step("Проверить, что бронь создана"):
        assert_booking_created(response, validated, new_booking)


@pytest.mark.regression
@allure.title("Получение брони по ID")
def test_get_booking_by_id(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=True)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    with allure.step("Получение бронирования по ID"):
        response, model = api.booking.get_by_id(created.bookingid, validate=True)

    with allure.step("Проверить, что данные брони совпали"):
        assert_booking_get(response, model, new_booking)


@pytest.mark.regression
@allure.title("Список бронирований содержит созданную бронь")
def test_list_bookings_contains_created(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=False)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    with allure.step("Получение списка бронирований"):
        list_response, booking_ids = api.booking.list(validate=True)

    ids = [item.bookingid for item in booking_ids] if booking_ids is not None else []
    with allure.step("Проверить, что созданная бронь есть в списке"):
        assert_booking_in_list(list_response, ids, created.bookingid)


@pytest.mark.regression
@allure.title("Полное обновление брони (PUT)")
def test_update_booking_put(api, set_token, cleanup):
    original_booking = _make_booking(with_additional=True)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(original_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    updated_booking = original_booking.model_copy(
        update={
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
        }
    )

    with allure.step("Обновление бронирования (PUT)"):
        response, model = api.booking.update_put(
            created.bookingid,
            updated_booking,
            token=set_token,
            validate=True,
        )

    with allure.step("Проверить, что бронь обновлена"):
        assert_booking_updated(response, model, updated_booking)


@pytest.mark.regression
@allure.title("Частичное обновление брони (PATCH)")
def test_update_booking_patch(api, set_token, cleanup):
    original_booking = _make_booking(with_additional=True)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(original_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    patch_payload: dict[str, Any] = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
    }

    with allure.step("Обновление бронирования (PATCH)"):
        response, model = api.booking.update_patch(
            created.bookingid,
            patch_payload,
            token=set_token,
            validate=True,
        )

    expected = original_booking.model_copy(update=patch_payload)
    with allure.step("Проверить, что бронь обновлена"):
        assert_booking_updated(response, model, expected)


@pytest.mark.regression
@allure.title("Удаление брони")
def test_delete_booking(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=False)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    with allure.step("Удаление бронирования"):
        delete_response, _ = api.booking.remove(
            created.bookingid,
            token=set_token,
        )

    with allure.step("Проверка удаления брони"):
        get_response, _ = api.booking.get_by_id(
            created.bookingid,
            validate=False,
        )

    with allure.step("Проверить, что бронь удалена"):
        assert_booking_deleted(delete_response)
        assert_not_found(get_response)

    cleanup.clear()


@pytest.mark.regression
@allure.title("Запрос несуществующего бронирования")
def test_booking_not_found(api, test_data):
    with allure.step("GET несуществующей брони"):
        booking_id = test_data["booking"]["non_existent_id"]
        response, _ = api.booking.get_by_id(booking_id, validate=False)

    with allure.step("Проверить, что бронь не найдена"):
        assert_not_found(response)


@pytest.mark.regression
@allure.title("Удаление без токена запрещено")
def test_booking_forbidden_without_token(api, set_token, cleanup):
    new_booking = _make_booking(with_additional=False)

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(new_booking, validate=True)
        cleanup.append(lambda: _cleanup_booking(api, created.bookingid, set_token))

    with allure.step("Попытка удаления без токена"):
        response, _ = api.booking.remove(created.bookingid)

    with allure.step("Проверить, что удаление без токена запрещено"):
        assert_forbidden(response)
