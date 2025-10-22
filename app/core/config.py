from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Bus Booking System"
    JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()
