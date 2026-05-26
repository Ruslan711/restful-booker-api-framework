from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


def generate_booking_payload(
    with_additional: bool = True,
    bad_dates: bool = False,
):

    checkin = datetime.now().date()
    checkout = checkin + timedelta(days=3)

    if bad_dates:
        checkout = checkin - timedelta(days=1)

    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(50, 500),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": str(checkin),
            "checkout": str(checkout),
        },
    }

    if with_additional:
        payload["additionalneeds"] = "Buggy"

    return payload