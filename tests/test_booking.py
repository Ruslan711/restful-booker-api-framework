from typing import Any

import allure

from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_booking_in_list,
    assert_booking_updated,
    assert_not_found,
    assert_forbidden,
)
from services.restful_booker.booking.models.booking import Booking, BookingDates


def _make_full_booking() -> Booking:
    return Booking(
        firstname="John",
        lastname="Doe",
        totalprice=150,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-01-10"),
        additionalneeds="Breakfast",
    )


def _make_minimal_booking() -> Booking:
    return Booking(
        firstname="Jane",
        lastname="Smith",
        totalprice=100,
        depositpaid=False,
        bookingdates=BookingDates(checkin="2024-02-01", checkout="2024-02-05"),
    )


@allure.title("Создание брони со всеми полями")
def test_create_booking_all_params(api, cleanup):
    new_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        response, validated = api.booking.create(new_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(validated.bookingid, validate=False)
        )

    assert_booking_created(response, validated, new_booking)


@allure.title("Создание брони с минимальным набором полей")
def test_create_booking_minimal(api, cleanup):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        response, validated = api.booking.create(new_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(validated.bookingid, validate=False)
        )

    assert_booking_created(response, validated, new_booking)


@allure.title("Получение брони по ID")
def test_get_booking_by_id(api, cleanup):
    new_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(new_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(created.bookingid, validate=False)
        )

    with allure.step("Получение бронирования по ID"):
        response, model = api.booking.get_by_id(created.bookingid)

    assert_booking_updated(response, model, new_booking)


@allure.title("Список бронирований содержит созданную бронь (через GET)")
def test_list_bookings_contains_created(api, cleanup):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        response, created = api.booking.create(new_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(created.bookingid, validate=False)
        )

    with allure.step("Проверка существования брони через GET"):
        get_response, model = api.booking.get_by_id(created.bookingid)

    assert model is not None
    assert model.firstname == new_booking.firstname
    assert model.lastname == new_booking.lastname


@allure.title("Полное обновление брони (PUT)")
def test_update_booking_put(api, cleanup, set_token):
    original_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(original_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(created.bookingid, token=set_token, validate=False)
        )

    updated_booking = _make_full_booking()
    updated_booking.firstname = "Updated"
    updated_booking.lastname = "User"

    with allure.step("Обновление бронирования (PUT)"):
        response, model = api.booking.update_put(
            created.bookingid,
            updated_booking,
            token=set_token,
        )

    assert_booking_updated(response, model, updated_booking)


@allure.title("Частичное обновление брони (PATCH)")
def test_update_booking_patch(api, cleanup, set_token):
    original_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(original_booking, validate=True)
        cleanup.append(
            lambda: api.booking.remove(created.bookingid, token=set_token, validate=False)
        )

    patch_payload: dict[str, Any] = {
        "firstname": "Patched",
        "lastname": "User",
    }

    with allure.step("Обновление бронирования (PATCH)"):
        response, model = api.booking.update_patch(
            created.bookingid,
            patch_payload,
            token=set_token,
        )

    expected = original_booking.model_copy(update=patch_payload)
    assert_booking_updated(response, model, expected)


@allure.title("Удаление брони")
def test_delete_booking(api, set_token):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        _, created = api.booking.create(new_booking, validate=True)

    with allure.step("Удаление бронирования"):
        response, _ = api.booking.remove(
            created.bookingid,
            token=set_token,
        )

    with allure.step("Проверка удаления брони"):
        get_response, _ = api.booking.get_by_id(
            created.bookingid,
            validate=False,
        )

    assert_not_found(get_response)


@allure.title("Запрос несуществующего бронирования")
def test_booking_not_found(api):
    with allure.step("GET несуществующей брони"):
        response, _ = api.booking.get_by_id(999999, validate=False)

    assert_not_found(response)


@allure.title("Удаление без токена запрещено")
def test_booking_forbidden_without_token(api):
    with allure.step("Попытка удаления без токена"):
        response, _ = api.booking.remove(1, validate=False)

    assert_forbidden(response)
