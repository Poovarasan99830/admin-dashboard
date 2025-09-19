from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP
from sqlalchemy.sql import func
from src.common.database import Base


class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(Enum("active", "suspended", name="provider_status"), default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class FlaggedBooking(Base):
    __tablename__ = "flagged_bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum("pending", "reviewed", "resolved", name="flag_status"), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    resolved_at = Column(TIMESTAMP, nullable=True)
