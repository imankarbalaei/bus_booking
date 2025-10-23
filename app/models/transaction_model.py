import enum
from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class TransactionType(enum.Enum):
    topup = "topup"
    direct_payment = "direct_payment"
    refund = "refund"

class PaymentMethod(enum.Enum):
    wallet = "wallet"
    gateway = "gateway"
    manual = "manual"

class TransactionStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="SET NULL"), nullable=True)
    related_booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Integer, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.pending, nullable=False)
    wallet_balance_after = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
    wallet = relationship("Wallet", back_populates="transactions")
    booking = relationship("Booking", back_populates="transaction")
