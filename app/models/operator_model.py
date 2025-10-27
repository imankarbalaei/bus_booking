from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from .base import TimestampMixin

class Operator(Base, TimestampMixin):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_name = Column(String(255), nullable=False)
    license_number = Column(String(100), nullable=False)
