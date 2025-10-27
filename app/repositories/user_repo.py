from app.db.database import fetchrow, execute
from app.schemas.user_schema import UserCreate

class UserRepository:
    async def get_by_phone(self, phone_number: str):
        query = "SELECT * FROM users WHERE phone_number=$1 AND deleted_at IS NULL"
        return await fetchrow(query, phone_number)

    async def get_by_id(self, user_id: int):
        query = "SELECT * FROM users WHERE id=$1 AND deleted_at IS NULL"
        return await fetchrow(query, user_id)

    async def create(self, user: UserCreate, hashed_password: str):
        query = """
            INSERT INTO users(full_name, phone_number, hashed_password, is_active, is_admin)
            VALUES($1, $2, $3, true, false)
            RETURNING id, full_name, phone_number
        """
        return await fetchrow(query, user.full_name, user.phone_number, hashed_password)


user_repo = UserRepository()
