# from pydantic import BaseModel, Field
# from datetime import datetime
#
# class BusCreate(BaseModel):
#     operator_id: int
#     plate_number: str = Field(..., example="12A34567")
#     capacity: int = Field(..., gt=0, le=60)
#     route_id: int
#
# class BusResponse(BaseModel):
#     id: int
#     plate_number: str
#     capacity: int
#     route_id: int
#
#     model_config = {"from_attributes": True}
#
#
# class TripCreate(BaseModel):
#     bus_id: int
#     departure_time: datetime
#     arrival_time: datetime
#     price: int = Field(..., gt=0)
#
# class TripResponse(BaseModel):
#     id: int
#     bus_id: int
#     departure_time: datetime
#     arrival_time: datetime
#     price: int
#
#     model_config = {"from_attributes": True}
