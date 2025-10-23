from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    province_name = Column(String, nullable=False)
    cities = relationship("City", back_populates="province")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"))

    province = relationship("Province", back_populates="cities")