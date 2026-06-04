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
        f"{message}\nExpected: {expected}\nActual: {actual}"
    )


@allure.step("Проверка: бронирование создано")
def assert_booking_created(
    response: Response,
    validated: BookingCreateResponse | None,
    expected_data: Booking | Mapping[str, Any],
) -> None:
    assert_status_code(response, 200)

    assert validated is not None, "BookingCreateResponse не должен быть None"

    expected = _booking_to_dict(expected_data)
    actual = validated.booking.model_dump()

    _assert_dicts_equal(
        actual=actual,
        expected=expected,
        message="Данные созданного бронирования не совпадают",
    )


@allure.step("Проверка: бронирование обновлено")
def assert_booking_updated(
    response: Response,
    validated: Booking | None,
    expected_data: Booking | Mapping[str, Any],
) -> None:
    assert_status_code(response, 200)

    assert validated is not None, "Booking не должен быть None"

    expected = _booking_to_dict(expected_data)
    actual = validated.model_dump()

    _assert_dicts_equal(
        actual=actual,
        expected=expected,
        message="Данные обновлённого бронирования не совпадают",
    )


@allure.step("Проверка: бронирование в списке")
def assert_booking_in_list(
    response: Response,
    validated: Sequence[int] | None,
    booking_id: int,
) -> None:
    assert_status_code(response, 200)

    assert validated is not None, "Список ID не должен быть None"

    assert booking_id in validated, (
        f"booking_id={booking_id} отсутствует в списке: {list(validated)}"
    )


@allure.step("Проверка: Forbidden (403)")
def assert_forbidden(response: Response) -> None:
    """Ожидаем HTTP 403 Forbidden."""
    assert_status_code(response, 403)


@allure.step("Проверка: Not Found (404)")
def assert_not_found(response: Response) -> None:
    """Статус 404 Not Found."""
    assert_status_code(response, 404)


@allure.step("Проверка, что бронирование получено (GET)")
def assert_booking_get(
    response: Response,
    validated: Booking | None,
    expected_data: Booking | Mapping[str, Any],
) -> None:
    """Статус 200 и тело бронирования совпадает с ожидаемым."""
    assert_status_code(response, 200)

    assert validated is not None, "Ожидали валидированную модель Booking, но получили None"

    expected = _booking_to_dict(expected_data)
    actual = validated.model_dump()
    assert actual == expected, "Данные полученного бронирования не совпадают с ожидаемыми"


@allure.step("Проверка, что бронирование удалено")
def assert_booking_deleted(response: Response) -> None:
    """Статус успешного удаления (200, 201 или 204)."""
    actual = response.status_code
    assert actual in (200, 201, 204), (
        f"Ожидали статус удаления 200/201/204, но получили {actual}"
    )
