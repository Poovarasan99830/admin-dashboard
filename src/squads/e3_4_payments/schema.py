from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class FlagStatus(str, Enum):
    pending = "pending"
    reviewed = "reviewed"
    cleared = "cleared"

class FlaggedOut(BaseModel):
    id: UUID
    transaction_id: UUID
    flagged_reason: str
    status: FlagStatus
    flagged_at: datetime

    class Config:
        orm_mode = True

class DisputeResolution(BaseModel):
    resolution: str
    resolved_by: UUID
