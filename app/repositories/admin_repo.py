from app.db.database import fetch, fetchrow, execute
from typing import Optional, List

class AdminRepository:

    @staticmethod
    async def create_bus(operator_id: int, plate_number: str, capacity: int, route_id: int) -> dict:
        query = """
        INSERT INTO buses (operator_id, plate_number, capacity, route_id)
        VALUES ($1, $2, $3, $4)
        RETURNING id, operator_id, plate_number, capacity, route_id
        """
        return await fetchrow(query, operator_id, plate_number, capacity, route_id)

    @staticmethod
    async def get_bus_by_plate(plate_number: str) -> Optional[dict]:
        return await fetchrow("SELECT * FROM buses WHERE plate_number=$1", plate_number)

    @staticmethod
    async def get_all_buses() -> List[dict]:
        query = """
            SELECT 
                b.id AS bus_id,
                b.plate_number,
                b.capacity,
                r.id AS route_id,
                c1.id AS origin_city_id,
                c1.city_name AS origin_city,
                c2.id AS destination_city_id,
                c2.city_name AS destination_city,
                r.distance_km
            FROM buses b
            LEFT JOIN routes r ON b.route_id = r.id
            LEFT JOIN cities c1 ON r.origin_city_id = c1.id
            LEFT JOIN cities c2 ON r.destination_city_id = c2.id
            ORDER BY b.id DESC;
            """
        return await fetch(query)

    @staticmethod
    async def get_bus_by_id(bus_id: int):
        query = "SELECT id, route_id, capacity FROM buses WHERE id = $1"
        return await fetchrow(query, bus_id)
