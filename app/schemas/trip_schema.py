from pydantic import BaseModel
from typing import List

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
