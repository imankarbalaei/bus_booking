from app.db.database import fetchrow, execute

class WalletRepository:
    async def create(self, user_id: int, initial_balance: int = 0):
        query = """
            INSERT INTO wallets(user_id, balance)
            VALUES($1, $2)
            RETURNING id, user_id, balance
        """
        return await fetchrow(query, user_id, initial_balance)

    async def get_by_user_id(self, user_id: int):
        query = "SELECT * FROM wallets WHERE user_id=$1 AND deleted_at IS NULL"
        return await fetchrow(query, user_id)

    async def update_balance(self, wallet_id: int, new_balance: int):
        query = "UPDATE wallets SET balance=$1, updated_at=now() WHERE id=$2"
        return await execute(query, new_balance, wallet_id)

wallet_repo=WalletRepository()