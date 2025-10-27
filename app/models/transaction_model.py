from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.db.database import Base
from .base import TimestampMixin
import enum

class TransactionType(str, enum.Enum):
    debit = "debit"
    credit = "credit"

class PaymentMethod(str, enum.Enum):
    card = "card"
    wallet = "wallet"

class TransactionStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="SET NULL"))
    related_booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"))
    amount = Column(Integer, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)
    wallet_balance_after = Column(Integer, nullable=False)
