from typing import List
from app.repositories.trips_repo import TripsRepo
from app.schemas.trip_schema import TripResponse, TripCreate
from app.repositories.admin_repo import AdminRepository
from fastapi import HTTPException, status

class TripsService:
    @staticmethod
    async def list_available_trips(origin_id: int = None,
                                   destination_id: int = None,
                                   sort: str = "cheapest"):
        rows = await TripsRepo.get_available_trips(origin_id, destination_id, sort)
        results = []

        for row in rows:
            results.append({
                "trip_id": row["trip_id"],
                "bus_id": row["bus_id"],
                "price": row["price"],
                "status": row["status"],
                "departure_time": row["departure_time"].isoformat(),
                "arrival_time": row["arrival_time"].isoformat(),
                "origin": {"id": row["origin_id"], "name": row["origin_name"]},
                "destination": {"id": row["destination_id"], "name": row["destination_name"]},
                "available_seats_count": row["available_seats_count"],
                "available_seats": row["available_seats"]  # این خودش یک لیست از seat_number هست
            })

        return {
            "status": "success",
            "count": len(results),
            "results": results
        }

    @staticmethod
    async def create_trip(data: TripCreate) -> TripResponse:

        bus = await AdminRepository.get_bus_by_id(data.bus_id)
        if not bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with id={data.bus_id} not found"
            )


        if bus["route_id"] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bus must be assigned to a route before scheduling trips"
            )


        trip = await TripsRepo.create_trip(
            bus_id=data.bus_id,
            departure_time=data.departure_time,
            arrival_time=data.arrival_time,
            price=data.price,
        )

        return TripResponse(**trip)
