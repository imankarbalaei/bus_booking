from fastapi import APIRouter, Query
from typing import Optional
from app.services.trip_service import TripsService
from app.schemas.trip_schema import TripsListResponse

router = APIRouter(tags=["trips"])

@router.get("/", response_model=TripsListResponse)
async def get_trips(origin_id: Optional[int] = Query(None),
                    destination_id: Optional[int] = Query(None),
                    sort: Optional[str] = Query("cheapest", regex="^(cheapest|expensive)$")):
    return await TripsService.list_available_trips(origin_id, destination_id, sort)
