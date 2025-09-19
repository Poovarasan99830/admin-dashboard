from sqlalchemy import Column, Integer, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from src.common.database import Base


class AdminAction(Base):
    __tablename__ = "admin_actions"
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    action = Column(Enum("suspend", "restore", name="admin_action"), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
