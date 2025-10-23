import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class BookingStatus(enum.Enum):
    booked = "booked"
    canceled = "canceled"

class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.booked, nullable=False)
    booking_time = Column(DateTime(timezone=True), server_default=func.now())
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)

    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
    transaction = relationship("Transaction", back_populates="booking")
