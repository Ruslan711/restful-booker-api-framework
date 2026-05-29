from typing import Tuple

from requests import Response

from services.base_api import BaseAPI
from services.restful_booker.booking.models.booking import (
    Booking,
    BookingCreateResponse,
)
from services.restful_booker.booking.models.booking_list import BookingListItem
from services.restful_booker.booking.models.booking_patch import BookingPatch


class BookingClient(BaseAPI):

    def create(
        self,
        payload: Booking,
        validate: bool = True,
    ) -> Tuple[Response, BookingCreateResponse | None]:
        response = self.post("/booking", json=payload.model_dump())

        if not validate:
            return response, None

        return response, BookingCreateResponse.model_validate_json(response.text)

    def get_by_id(
        self,
        booking_id: int,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.get(f"/booking/{booking_id}")

        if not validate:
            return response, None

        return response, Booking.model_validate_json(response.text)

    def list(
        self,
        validate: bool = True,
    ) -> Tuple[Response, list[BookingListItem] | None]:
        response = self.get("/booking")

        if not validate:
            return response, None

        # Валидация через pydantic модель
        items = [BookingListItem.model_validate(item) for item in response.json()]
        return response, items

    def update_put(
        self,
        booking_id: int,
        payload: Booking,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.put(f"/booking/{booking_id}", json=payload.model_dump())

        if not validate:
            return response, None

        return response, Booking.model_validate_json(response.text)

    def update_patch(
        self,
        booking_id: int,
        payload: BookingPatch,
        validate: bool = True,
    ) -> Tuple[Response, Booking | None]:
        response = self.patch(
            f"/booking/{booking_id}",
            json=payload.model_dump(exclude_unset=True),
        )

        if not validate:
            return response, None

        return response, Booking.model_validate_json(response.text)

    def remove(
        self,
        booking_id: int,
    ) -> Tuple[Response, None]:
        response = self.delete(f"/booking/{booking_id}")
        return response, None
