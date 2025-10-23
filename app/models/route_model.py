from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    origin_city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    destination_city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    distance_km = Column(Integer, nullable=False)

    origin_city = relationship("City", foreign_keys=[origin_city_id])
    destination_city = relationship("City", foreign_keys=[destination_city_id])
    buses = relationship("Bus", back_populates="route", cascade="all, delete-orphan")


