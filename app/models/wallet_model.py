from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base
from .base import TimestampMixin

class Wallet(Base, TimestampMixin):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Integer, nullable=False, default=0)
