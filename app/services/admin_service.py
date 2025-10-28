from fastapi import HTTPException, status
from app.repositories.admin_repo import AdminRepository
from app.schemas.bus_schema import BusCreate, BusResponse
from typing import List
from app.repositories.operator_repo import OperatorRepository
from app.repositories.route_repo import RouteRepository


class AdminService:

    @staticmethod
    async def create_bus(bus_data: BusCreate) -> BusResponse:
        # چک وجود operator
        operator = await OperatorRepository.get_by_id(bus_data.operator_id)
        if not operator:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Operator with id={bus_data.operator_id} not found"
            )

        # چک وجود route
        route = await RouteRepository.get_by_id(bus_data.route_id)
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route with id={bus_data.route_id} not found"
            )

        # چک پلاک تکراری
        existing = await AdminRepository.get_bus_by_plate(bus_data.plate_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bus with this plate number already exists"
            )

        # ایجاد اتوبوس
        new_bus = await AdminRepository.create_bus(
            operator_id=bus_data.operator_id,
            plate_number=bus_data.plate_number,
            capacity=bus_data.capacity,
            route_id=bus_data.route_id,
        )

        return BusResponse(**new_bus)

    @staticmethod
    async def list_buses() -> List[BusResponse]:
        buses = await AdminRepository.get_all_buses()
        return [BusResponse(**b) for b in buses]
