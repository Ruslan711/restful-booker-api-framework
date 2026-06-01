from services.restful_booker.booking.assertions import (
    assert_booking_created,
    assert_not_found,
)
from services.restful_booker.booking.models.booking import Booking, BookingDates


def test_booking_create_and_cleanup(restful_booker_api, cleanup, set_token):
    payload = Booking(
        firstname="John",
        lastname="Doe",
        totalprice=100,
        depositpaid=True,
        bookingdates=BookingDates(
            checkin="2025-01-01",
            checkout="2025-01-10",
        ),
        additionalneeds="Breakfast",
    )

    response, validated = restful_booker_api.booking.create(payload)

    cleanup.append(
        lambda: restful_booker_api.booking.remove(
            validated.bookingid,
            token=set_token,
        )
    )

    assert_booking_created(response, validated, payload)


def test_booking_not_found(restful_booker_api, test_data):
    """Запрос несуществующего бронирования возвращает 404."""
    booking_id = test_data["booking"]["non_existent_id"]

    response, _ = restful_booker_api.booking.get_by_id(
        booking_id,
        validate=False,
    )

    assert_not_found(response)
