from fastapi import FastAPI
from app.api.routers import api_router

app = FastAPI(title="Bus Booking System")
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Bus Booking System is running "}

