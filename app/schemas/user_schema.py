from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr | None = None
    password: str


    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if not value.startswith("09"):
            raise ValueError("Phone number must start with '09'.")
        if len(value) != 11:
            raise ValueError("Phone number must be exactly 11 digits long.")
        return value



class UserLogin(BaseModel):
    phone_number: str
    password: str

    @validator("phone_number")
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if not value.startswith("09"):
            raise ValueError("Phone number must start with '09'.")
        if len(value) != 11:
            raise ValueError("Phone number must be exactly 11 digits long.")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str
