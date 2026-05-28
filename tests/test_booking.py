from typing import Any

import allure

from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_booking_in_list,
    assert_booking_updated,
    assert_forbidden,
    assert_not_found,
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
        if validated is not None:
            cleanup.append(lambda: api.booking.remove(validated.bookingid, validate=False))

    assert_booking_created(response, validated, new_booking)


@allure.title("Создание брони с минимальным набором полей")
def test_create_booking_minimal(api, cleanup):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        response, validated = api.booking.create(new_booking, validate=True)
        if validated is not None:
            cleanup.append(lambda: api.booking.remove(validated.bookingid, validate=False))

    assert_booking_created(response, validated, new_booking)


@allure.title("Получение брони по ID")
def test_get_booking_by_id(api, cleanup):
    new_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(new_booking, validate=True)
        assert_booking_created(create_response, created, new_booking)

    booking_id = created.bookingid  # type: ignore[union-attr]
    cleanup.append(lambda: api.booking.remove(booking_id, validate=False))

    with allure.step("Получение бронирования по ID"):
        response, model = api.booking.get_by_id(booking_id)

    assert_booking_updated(response, model, new_booking)


@allure.title("Список бронирований содержит созданную бронь")
def test_list_bookings_contains_created(api, cleanup):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(new_booking, validate=True)
        assert_booking_created(create_response, created, new_booking)

    booking_id = created.bookingid  # type: ignore[union-attr]
    cleanup.append(lambda: api.booking.remove(booking_id, validate=False))

    with allure.step("Получение списка бронирований"):
        response, booking_ids = api.booking.list()

    assert_booking_in_list(response, booking_ids, booking_id)


@allure.title("Полное обновление брони (PUT)")
def test_update_booking_put(api, cleanup, set_token):
    original_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(original_booking, validate=True)
        assert_booking_created(create_response, created, original_booking)

    booking_id = created.bookingid  # type: ignore[union-attr]
    cleanup.append(lambda: api.booking.remove(booking_id, token=set_token, validate=False))

    updated_booking = _make_full_booking()
    updated_booking.firstname = "Updated"
    updated_booking.lastname = "User"

    with allure.step("Полное обновление бронирования (PUT)"):
        response, model = api.booking.update_put(booking_id, updated_booking, token=set_token)

    assert_booking_updated(response, model, updated_booking)


@allure.title("Частичное обновление брони (PATCH)")
def test_update_booking_patch(api, cleanup, set_token):
    original_booking = _make_full_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(original_booking, validate=True)
        assert_booking_created(create_response, created, original_booking)

    booking_id = created.bookingid  # type: ignore[union-attr]
    cleanup.append(lambda: api.booking.remove(booking_id, token=set_token, validate=False))

    patch_payload: dict[str, Any] = {"firstname": "Patched", "lastname": "User"}

    with allure.step("Частичное обновление бронирования (PATCH)"):
        response, model = api.booking.update_patch(booking_id, patch_payload, token=set_token)

    expected = original_booking.model_copy(update=patch_payload)
    assert_booking_updated(response, model, expected)


@allure.title("Удаление брони")
def test_delete_booking(api, set_token):
    new_booking = _make_minimal_booking()

    with allure.step("Создание бронирования"):
        create_response, created = api.booking.create(new_booking, validate=True)
        assert_booking_created(create_response, created, new_booking)

    booking_id = created.bookingid  # type: ignore[union-attr]

    with allure.step("Удаление бронирования"):
        response, _ = api.booking.remove(booking_id, token=set_token)



@allure.title("Запрос несуществующего бронирования возвращает 404")
def test_booking_not_found(api, test_data):
    booking_id = test_data["booking"]["non_existent_id"]

    with allure.step("Запрос несуществующего бронирования"):
        response, _ = api.booking.get_by_id(booking_id, validate=False)

    assert_not_found(response)


@allure.title("Запрос без авторизации возвращает 403 Forbidden")
def test_booking_forbidden_without_token(api, test_data):
    booking_id = test_data["booking"]["non_existent_id"]

    with allure.step("Удаление без токена"):
        response, _ = api.booking.remove(booking_id, validate=False)

    assert_forbidden(response)
