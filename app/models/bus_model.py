from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plate_number = Column(String(8), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="SET NULL"), nullable=True)

    route = relationship("Route", back_populates="buses")
    operator = relationship("User", back_populates="buses")
    trips = relationship("Trip", back_populates="bus", cascade="all, delete-orphan")

