def test_booking_not_found(restful_booker_api, test_data):
    """Запрос несуществующего бронирования возвращает 404."""
    booking_id = test_data["booking"]["non_existent_id"]

    response, _ = restful_booker_api.booking.get_by_id(booking_id, validate=False)

    assert response.status_code == 404