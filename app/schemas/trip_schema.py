from typing import List
from pydantic import BaseModel, Field, validator
from datetime import datetime
from app.models.trip_model import TripStatus


class CityResponse(BaseModel):
    id: int
    name: str

class TripResponse(BaseModel):
    trip_id: int
    bus_id: int
    price: int
    status: str
    departure_time: str
    arrival_time: str
    origin: CityResponse
    destination: CityResponse
    available_seats_count: int
    available_seats: List[int]

class TripsListResponse(BaseModel):
    status: str
    count: int
    results: List[TripResponse]


class TripCreate(BaseModel):
    bus_id: int = Field(..., gt=0)
    departure_time: datetime
    arrival_time: datetime
    price: int = Field(..., gt=0)

    @validator("arrival_time")
    def arrival_after_departure(cls, v, values):
        dep = values.get("departure_time")
        if dep and v <= dep:
            raise ValueError("arrival_time must be after departure_time")
        return v

    @validator("departure_time", "arrival_time")
    def must_be_in_future(cls, v):
        from datetime import datetime, timezone
        if v <= datetime.now(timezone.utc):
            raise ValueError("departure/arrival time must be in the future")
        return v


class TripResponse(BaseModel):
    id: int
    bus_id: int
    departure_time: datetime
    arrival_time: datetime
    price: int
    status: TripStatus

    class Config:
        orm_mode = True

