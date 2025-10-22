from fastapi import FastAPI

app = FastAPI(title="Bus Booking System")

@app.get("/")
async def root():
    return {"message": "Bus Booking System is running "}
