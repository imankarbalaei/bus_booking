from fastapi import FastAPI
from app.api.routers import api_router as api_router_v1
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Bus Booking System")
app.include_router(api_router_v1)

@app.get("/")
async def root():
    return {"message": "Bus Booking System is running "}

