from typing import List, Tuple

from requests import Response

from config.environments import EnvironmentConfig
from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import (
    Booking,
    BookingCreateResponse,
)


class BookingClient(BaseAPI):
    def __init__(self, env_config: EnvironmentConfig) -> None:
        super().__init__(env_config)

    def create(
        self,
        payload: Booking,
        validate: bool = True,
    ) -> Tuple[Response, BookingCreateResponse | None]:
        response = self.post("/booking", json=payload.model_dump())

        if not validate:
            return response, None

        model = BookingCreateResponse.model_validate_json(response.text)
        return response, model

    def get_by_id(
        self,
        booking_id: int,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.get(f"/booking/{booking_id}")

        if not validate:
            return response, None

        model = Booking.model_validate_json(response.text)
        return response, model

    def list(
        self,
        validate: bool = True,
        **params: str,
    ) -> Tuple[Response, List[int] | None]:
        response = self.get("/booking", params=params or None)

        if not validate:
            return response, None

        data = response.json()
        booking_ids = [item["bookingid"] for item in data]
        return response, booking_ids

    def update_put(
        self,
        booking_id: int,
        payload: Booking,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.put(f"/booking/{booking_id}", json=payload.model_dump())

        if not validate:
            return response, None

        model = Booking.model_validate_json(response.text)
        return response, model

    def update_patch(
        self,
        booking_id: int,
        payload: dict,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.patch(f"/booking/{booking_id}", json=payload)

        if not validate:
            return response, None

        model = Booking.model_validate_json(response.text)
        return response, model

    def remove(
        self,
        booking_id: int,
        validate: bool = True,
    ) -> Tuple[Response, None]:
        response = self.delete(f"/booking/{booking_id}")

        if validate:
            assert response.status_code in (200, 201, 204)

        return response, None