from app.db.database import fetchrow

class RouteRepository:
    @staticmethod
    async def get_by_id(route_id: int):
        query = "SELECT * FROM routes WHERE id = $1"
        return await fetchrow(query, route_id)
