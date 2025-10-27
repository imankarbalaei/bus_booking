from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from .base import TimestampMixin

class Bus(Base, TimestampMixin):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    plate_number = Column(String(8), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"))
