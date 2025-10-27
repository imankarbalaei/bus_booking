from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base
from .base import TimestampMixin

class Route(Base, TimestampMixin):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    origin_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    destination_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    distance_km = Column(Integer, nullable=False)
