from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from app.db.database import Base
from .base import TimestampMixin
import enum

class TripStatus(str, enum.Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"

class Trip(Base, TimestampMixin):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    departure_time = Column(DateTime(timezone=True), nullable=False)
    arrival_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Enum(TripStatus), nullable=False)
