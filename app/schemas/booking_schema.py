from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class BookingStatus(str, Enum):
    booked = "booked"
    canceled = "canceled"

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"

class BookingCreate(BaseModel):
    trip_id: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    trip_id: int
    status: BookingStatus
    payment_status: PaymentStatus
    booking_time: datetime

    model_config = {
        "from_attributes": True
    }
