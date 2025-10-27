# app/api/v1/booking_router.py
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.booking_schema import BookingRequest, BookingResponse, CancelRequest
from app.services.booking_service import BookingService
from app.core.dependencies import get_current_user  # فرضا dependency ای که user dict برمیگردونه

router = APIRouter(tags=["bookings"])

@router.post("/reserve", response_model=BookingResponse)
async def reserve(req: BookingRequest, current_user = Depends(get_current_user)):
    # validate seat_numbers length etc.
    booking_ids = await BookingService.book_seats(current_user["id"], req.trip_id, req.seat_numbers, req.pay_with_wallet)
    return {"booking_ids": booking_ids}

@router.post("/cancel")
async def cancel(req: CancelRequest, current_user = Depends(get_current_user)):

    from app.services.booking_service import BookingService
    await BookingService.cancel_booking(current_user["id"], req.booking_id)
    return {"status": "cancelled"}
