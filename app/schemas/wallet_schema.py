from pydantic import BaseModel

class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: int

    class Config:
        from_attributes = True