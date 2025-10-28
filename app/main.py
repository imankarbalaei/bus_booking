from fastapi import FastAPI
from app.db.database import connect_db, disconnect_db
from app.api.routers import api_router
from fastapi import  Depends
from app.core.dependencies import get_current_user
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Bus Booking System")

@app.on_event("startup")
async def startup():
    logger.info("Startup event triggered...")
    await connect_db()
    logger.info("Database pool connected successfully.")



@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown event triggered...")
    await disconnect_db()
    logger.info("Database pool disconnected.")

app.include_router(api_router, prefix="/v1")

@app.get("/v1/me")
async def read_me(current_user: dict = Depends(get_current_user)):
    return current_user

print("test")