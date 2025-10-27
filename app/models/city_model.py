from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from .base import TimestampMixin

class Province(Base, TimestampMixin):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True)
    province_name = Column(String, nullable=False)

class City(Base, TimestampMixin):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"))
