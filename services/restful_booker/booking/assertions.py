from typing import Any, Mapping, Sequence

import allure
from requests import Response

from services.restful_booker.booking.models.booking import (
    Booking,
    BookingCreateResponse,
)
from utils.assertions import assert_status_code


def _booking_to_dict(booking: Booking | Mapping[str, Any]) -> dict:
    """Приводит Booking или dict к обычному словарю."""
    if isinstance(booking, Booking):
        return booking.model_dump()
    return dict(booking)


def _assert_dicts_equal(actual: dict, expected: dict, message: str) -> None:
    assert actual == expected, (
        f"{message}\n"
        f"Expected: {expected}\n"
        f"Actual:   {actual}"
    )


@allure.step("Проверка, что бронирование создано")
def assert_booking_created(
    response: Response,
    validated: BookingCreateResponse | None,
    expected_data: Booking | Mapping[str, Any],
) -> None:
    """Статус 200 и тело созданного бронирования совпадает с expected_data."""
    assert_status_code(response, 200)

    assert validated is not None, (
        "Ожидали валидированную модель BookingCreateResponse, но получили None"
    )

    expected = _booking_to_dict(expected_data)
    actual = validated.booking.model_dump()

    _assert_dicts_equal(
        actual=actual,
        expected=expected,
        message="Данные созданного бронирования не совпадают с ожидаемыми.",
    )


@allure.step("Проверка, что бронирование обновлено")
def assert_booking_updated(
    response: Response,
    validated: Booking | None,
    expected_data: Booking | Mapping[str, Any],
) -> None:
    """Статус 200 и тело обновлённого бронирования совпадает с expected_data."""
    assert_status_code(response, 200)

    assert validated is not None, (
        "Ожидали валидированную модель Booking, но получили None"
    )

    expected = _booking_to_dict(expected_data)
    actual = validated.model_dump()

    _assert_dicts_equal(
        actual=actual,
        expected=expected,
        message="Данные обновлённого бронирования не совпадают с ожидаемыми.",
    )


@allure.step("Проверка, что бронирование присутствует в списке")
def assert_booking_in_list(
    response: Response,
    validated: Sequence[int] | None,
    booking_id: int,
) -> None:
    """Статус 200 и booking_id присутствует в списке ID."""
    assert_status_code(response, 200)

    assert validated is not None, (
        "Ожидали список ID бронирований, но получили None"
    )

    assert booking_id in validated, (
        f"Ожидали, что booking_id={booking_id} будет в списке, но его там нет.\n"
        f"Список ID: {list(validated)}"
    )


@allure.step("Проверка, что доступ запрещён (403 Forbidden)")
def assert_forbidden(response: Response) -> None:
    """Статус 403 Forbidden."""
    assert_status_code(response, 403)


@allure.step("Проверка, что ресурс не найден (404 Not Found)")
def assert_not_found(response: Response) -> None:
    """Статус 404 Not Found."""
    assert_status_code(response, 404)