from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Bus Booking System"
    SECRET_KEY: str
    ALGORITHM: ClassVar[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: ClassVar[int] = 60

    class Config:
        env_file = ".env"


settings = Settings()
