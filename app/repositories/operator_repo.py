from app.db.database import fetchrow

class OperatorRepository:
    @staticmethod
    async def get_by_id(operator_id: int):
        query = "SELECT * FROM operators WHERE id = $1"
        return await fetchrow(query, operator_id)
