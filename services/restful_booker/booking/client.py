from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import (
    Booking,
    BookingCreateResponse,
)


class BookingClient(BaseAPI):
    """Клиент для работы с бронированиями."""

    def create(
        self,
        booking: Booking,
        validate: bool = True,
    ) -> tuple[Response, BookingCreateResponse | None]:
        """Создать бронирование."""
        response = self.post("/booking", json=booking.model_dump())

        if not validate:
            return response, None

        model = BookingCreateResponse.model_validate_json(response.text)
        return response, model

    def get_by_id(
        self,
        booking_id: int,
        validate: bool = True,
    ) -> tuple[Response, Booking | None]:
        """Получить бронирование по ID."""
        response = self.get(f"/booking/{booking_id}")

        if not validate:
            return response, None

        model = Booking.model_validate_json(response.text)
        return response, model

    def remove(
        self,
        booking_id: int,
        token: str | None = None,
    ) -> tuple[Response, None]:
        """Удалить бронирование. Проверка статуса — в assertions-слое."""
        response = self.delete(
            f"/booking/{booking_id}",
            headers={"Cookie": f"token={token}"} if token else None,
        )
        return response, None
