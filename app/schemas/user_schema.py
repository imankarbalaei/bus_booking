from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    full_name: str = Field(..., example="Ali Reza")
    phone_number: str = Field(..., min_length=11, max_length=11, example="09123456789")
    password: str = Field(..., min_length=6, example="securepassword")

class UserResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
