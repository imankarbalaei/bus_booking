from typing import List
from app.repositories.trips_repo import TripsRepo
from app.schemas.trip_schema import TripResponse


class TripsService:
    @staticmethod
    async def list_available_trips(origin_id: int = None,
                                   destination_id: int = None,
                                   sort: str = "cheapest"):
        rows = await TripsRepo.get_available_trips(origin_id, destination_id, sort)
        trips_dict = {}
        for row in rows:
            trip_id = row["trip_id"]
            if trip_id not in trips_dict:
                trips_dict[trip_id] = {
                    "trip_id": trip_id,
                    "bus_id": row["bus_id"],
                    "price": row["price"],
                    "status": row["status"],
                    "departure_time": row["departure_time"].isoformat(),
                    "arrival_time": row["arrival_time"].isoformat(),
                    "origin": {"id": row["origin_id"], "name": row["origin_name"]},
                    "destination": {"id": row["destination_id"], "name": row["destination_name"]},
                    "available_seats": []
                }
            if row["seat_status"] == "available":
                trips_dict[trip_id]["available_seats"].append(row["seat_number"])

        results = []
        for t in trips_dict.values():
            t["available_seats_count"] = len(t["available_seats"])
            results.append(t)

        return {
            "status": "success",
            "count": len(results),
            "results": results
        }
