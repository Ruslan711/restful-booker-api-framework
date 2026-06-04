from pydantic import BaseModel, Field


class BookingListItem(BaseModel):
    """Модель элемента списка бронирований."""
    bookingid: int = Field(..., description="ID бронирования")
