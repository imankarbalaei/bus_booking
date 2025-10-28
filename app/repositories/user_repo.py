from app.schemas.user_schema import UserCreate
from app.db.database import fetchrow
class UserRepository:
    @staticmethod
    async def get_by_phone(phone_number: str):
        query = "SELECT * FROM users WHERE phone_number=$1 AND deleted_at IS NULL"
        return await fetchrow(query, phone_number)

    @staticmethod
    async def get_by_id(user_id: int):
        query = "SELECT * FROM users WHERE id=$1 AND deleted_at IS NULL"
        return await fetchrow(query, user_id)

    @staticmethod
    async def create(user: UserCreate, hashed_password: str):
        query = """
            INSERT INTO users(full_name, phone_number, hashed_password, is_active, is_admin)
            VALUES($1, $2, $3, true, false)
            RETURNING id, full_name, phone_number
        """
        return await fetchrow(query, user.full_name, user.phone_number, hashed_password)



