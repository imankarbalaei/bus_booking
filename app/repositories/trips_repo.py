from typing import List, Optional
from app.db.database import get_pool, fetchrow, fetch


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
                    COALESCE(
                        ARRAY_AGG(s.seat_number ORDER BY s.seat_number) 
                        FILTER (WHERE s.status = 'available'), '{}'
                    ) AS available_seats,
                    COALESCE(
                        COUNT(s.id) FILTER (WHERE s.status = 'available'), 0
                    ) AS available_seats_count
                FROM trips t
                JOIN buses b ON b.id = t.bus_id
                JOIN routes r ON r.id = b.route_id
                JOIN cities c_from ON r.origin_city_id = c_from.id
                JOIN cities c_to ON r.destination_city_id = c_to.id
                LEFT JOIN seats s ON s.trip_id = t.id
                WHERE t.status = 'scheduled'
                  AND t.departure_time > NOW()
            """

            params = []
            param_idx = 1
            if origin_id:
                query += f" AND r.origin_city_id = ${param_idx}"
                params.append(origin_id)
                param_idx += 1
            if destination_id:
                query += f" AND r.destination_city_id = ${param_idx}"
                params.append(destination_id)
                param_idx += 1

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

    @staticmethod
    async def create_trip(bus_id: int, departure_time, arrival_time, price: int):
        pool = await get_pool()
        async with pool.acquire() as conn:
            tr = conn.transaction()
            await tr.start()
            try:

                trip = await conn.fetchrow(
                    """
                    INSERT INTO trips (bus_id, departure_time, arrival_time, price, status)
                    VALUES ($1, $2, $3, $4, 'scheduled')
                    RETURNING id, bus_id, departure_time, arrival_time, price, status
                    """,
                    bus_id, departure_time, arrival_time, price
                )


                bus_row = await conn.fetchrow("SELECT capacity FROM buses WHERE id = $1", bus_id)
                if not bus_row:
                    raise ValueError("Bus not found")

                capacity = bus_row["capacity"]


                seat_records = [(trip["id"], i) for i in range(1, capacity + 1)]
                await conn.executemany(
                    "INSERT INTO seats (trip_id, seat_number, status) VALUES ($1, $2, 'available')",
                    seat_records
                )

                await tr.commit()
                return trip
            except Exception as e:
                await tr.rollback()
                raise e
        return await fetchrow(query, bus_id, departure_time, arrival_time, price)

    @staticmethod
    async def get_all_trips():
        return await fetch("SELECT * FROM trips ORDER BY departure_time DESC")

