
from pydantic import BaseModel, Field, constr
from typing import Optional

class BusCreate(BaseModel):
    operator_id: int = Field(..., example=1)
    plate_number: constr(min_length=8,max_length=8) = Field(..., example="12A12314")
    capacity: int = Field(..., ge=10, le=80)
    route_id: int = Field(..., example=2)

class BusResponse(BaseModel):
    id: int
    operator_id: int
    plate_number: str
    capacity: int
    route_id: int

    class Config:
        orm_mode = True
