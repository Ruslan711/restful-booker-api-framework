import allure
from services.restful_booker.booking.assertions import assert_not_found


@allure.title("Поиск несуществующего бронирования возвращает 404")
def test_booking_not_found(api, test_data):
    """Запрос несуществующего бронирования возвращает 404."""
    booking_id = test_data["booking"]["non_existent_id"]

    with allure.step("Запрос несуществующего бронирования"):
        response, _ = api.booking.get_by_id(booking_id, validate=False)

    assert_not_found(response)