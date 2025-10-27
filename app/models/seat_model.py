from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from app.db.database import Base
from .base import TimestampMixin
import enum

class SeatStatus(str, enum.Enum):
    available = "available"
    reserved = "reserved"
    cancelled = "cancelled"

class Seat(Base, TimestampMixin):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    status = Column(Enum(SeatStatus), default=SeatStatus.available, nullable=False)


