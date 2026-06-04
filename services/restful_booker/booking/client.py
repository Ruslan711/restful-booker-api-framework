from typing import Any

from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import (
    Booking,
    BookingCreateResponse,
)
from services.restful_booker.booking.models.booking_list import BookingListItem

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

    def list(
        self,
        validate: bool = True,
    ) -> tuple[Response, list[BookingListItem] | None]:
        """Получить список бронирований."""
        response = self.get("/booking")

        if not validate:
            return response, None

        items = [BookingListItem.model_validate(item) for item in response.json()]
        return response, items

    def update_put(
        self,
        booking_id: int,
        booking: Booking,
        token: str | None = None,
        validate: bool = True,
    ) -> tuple[Response, Booking | None]:
        """Полное обновление бронирования."""
        headers = {"Cookie": f"token={token}"} if token else None

        response = self.put(
            f"/booking/{booking_id}",
            json=booking.model_dump(),
            headers=headers,
        )

        if not validate:
            return response, None

        model = Booking.model_validate_json(response.text)
        return response, model

    def update_patch(
        self,
        booking_id: int,
        partial_data: dict[str, Any],
        token: str | None = None,
        validate: bool = True,
    ) -> tuple[Response, Booking | None]:
        """Частичное обновление бронирования."""
        headers = {"Cookie": f"token={token}"} if token else None

        response = self.patch(
            f"/booking/{booking_id}",
            json=partial_data,
            headers=headers,
        )

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
