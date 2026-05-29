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

    response, model = restful_booker_api.booking.create(payload)

    booking_id = model.bookingid

    cleanup.append(
        lambda: restful_booker_api.booking.remove(booking_id, token=set_token, validate=False)
    )

    assert_booking_created(response, model, payload)


def test_booking_not_found(restful_booker_api, test_data):
    booking_id = test_data["booking"]["non_existent_id"]

    response, _ = restful_booker_api.booking.get_by_id(
        booking_id,
        validate=False,
    )

    assert_not_found(response)
