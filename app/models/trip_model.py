import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class TripStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id", ondelete="CASCADE"), nullable=False)
    departure_time = Column(DateTime(timezone=True), nullable=False)
    arrival_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Enum(TripStatus), default=TripStatus.scheduled, nullable=False)

    bus = relationship("Bus", back_populates="trips")
    bookings = relationship("Booking", back_populates="trip")
