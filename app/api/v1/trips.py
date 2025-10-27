# # app/api/v1/trips.py
# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List
#
# from app.schemas.trip_schema import TripResponse
# from app.services.trip_service import TripService
# from app.db.database import get_session
#
# router = APIRouter(prefix="/trips", tags=["Trips"])
#
# @router.get("/", response_model=List[TripResponse])
# async def get_trips(
#     origin: str | None = Query(None),
#     destination: str | None = Query(None),
#     sort: str = Query("asc", regex="^(asc|desc)$"),
#     session: AsyncSession = Depends(get_session)
# ):
#     trips = await TripService.list_available_trips(session, origin, destination, sort)
#     return trips
