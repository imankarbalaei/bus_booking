from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.bus_schema import BusCreate, BusResponse
from app.services.admin_service import AdminService
from fastapi import APIRouter, Depends
from app.schemas.trip_schema import TripCreate, TripResponse
from app.services.trip_service import TripsService
from app.core.dependencies import admin_required

router = APIRouter()


@router.post("/create_bus", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
async def create_bus(bus_data: BusCreate, admin_user=Depends(admin_required)):
    return await AdminService.create_bus(bus_data)


@router.get("/list_buses", response_model=List[BusResponse])
async def list_buses( admin_user=Depends(admin_required)):
    return await AdminService.list_buses()


@router.post("/create_trip", response_model=TripResponse)
async def create_trip(
        trip_data: TripCreate,
        admin_user=Depends(admin_required)
):
    return await TripsService.create_trip(trip_data)


@router.get("/list_trips", response_model=list[TripResponse])
async def list_trips(admin_user=Depends(admin_required)):
    return await TripsService.list_trips()
