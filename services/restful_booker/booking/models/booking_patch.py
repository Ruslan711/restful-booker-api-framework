from typing import Optional
from pydantic import BaseModel


class BookingDatesPatch(BaseModel):
    checkin: Optional[str] = None
    checkout: Optional[str] = None


class BookingPatch(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    totalprice: Optional[int] = None
    depositpaid: Optional[bool] = None
    bookingdates: Optional[BookingDatesPatch] = None
    additionalneeds: Optional[str] = None
