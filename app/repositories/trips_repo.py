from typing import List, Optional
from app.db.database import get_pool


class TripsRepo:
    @staticmethod
    async def get_available_trips(origin_id: Optional[int] = None,
                                  destination_id: Optional[int] = None,
                                  sort: str = "cheapest"):
        pool = await get_pool()
        async with pool.acquire() as conn:
            query = """
                        SELECT 
                            t.id AS trip_id,
                            t.bus_id,
                            t.price,
                            t.status,
                            t.departure_time,
                            t.arrival_time,
                            c_from.id AS origin_id,
                            c_from.city_name AS origin_name,
                            c_to.id AS destination_id,
                            c_to.city_name AS destination_name,
                            ARRAY_AGG(s.seat_number ORDER BY s.seat_number) AS available_seats,
                            COUNT(s.id) AS available_seats_count
                        FROM trips t
                        JOIN routes r ON r.id = t.bus_id
                        JOIN cities c_from ON r.origin_city_id = c_from.id
                        JOIN cities c_to ON r.destination_city_id = c_to.id
                        JOIN seats s ON s.trip_id = t.id AND s.status = 'available'
                        WHERE 
                            t.status = 'scheduled'
                            AND t.departure_time > NOW()
                        """
            params = []
            if origin_id:
                query += " AND r.origin_city_id = $1"
                params.append(origin_id)
            if destination_id:
                param_idx = len(params) + 1
                query += f" AND r.destination_city_id = ${param_idx}"
                params.append(destination_id)

            query += """
                        GROUP BY 
                            t.id, t.bus_id, t.price, t.status, 
                            t.departure_time, t.arrival_time,
                            c_from.id, c_from.city_name,
                            c_to.id, c_to.city_name
                        """

            if sort == "cheapest":
                query += " ORDER BY t.price ASC"
            elif sort == "expensive":
                query += " ORDER BY t.price DESC"

            rows = await conn.fetch(query, *params)
            return rows
