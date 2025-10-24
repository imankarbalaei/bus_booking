from pydantic import BaseModel
from enum import Enum


class PaymentMethod(str, Enum):
    wallet = "wallet"
    gateway = "gateway"

class BookingCreate(BaseModel):
    trip_id: int
    payment_method: PaymentMethod

class BookingResponse(BaseModel):
    id: int
    trip_id: int
    user_id: int
    status: str
    payment_status: str
    amount: int

    model_config = {
        "from_attributes": True
    }

class BookingCancelResponse(BaseModel):
    id: int
    trip_id: int
    status: str
    payment_status: str
    refund_amount: int

    model_config = {"from_attributes": True}
