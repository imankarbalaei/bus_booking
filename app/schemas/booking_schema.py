from typing import Annotated,List
from pydantic import BaseModel, Field

class BookingRequest(BaseModel):
    trip_id: int
    seat_numbers: Annotated[list[int], Field(min_length=1)]# user can request multiple seats
    pay_with_wallet: bool = True  # if False -> simulate gateway

class BookingResponse(BaseModel):
    booking_ids: List[int]

class CancelRequest(BaseModel):
    booking_ids: List[int]

class TripFilter(BaseModel):
    origin_city_id: int | None = None
    destination_city_id: int | None = None
    sort: str | None = None

class CancelResponse(BaseModel):
    status: str
    wallet_balance: int
    cancelled_bookings: List[int]
