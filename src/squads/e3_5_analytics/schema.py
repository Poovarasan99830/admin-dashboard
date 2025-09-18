from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class AnalyticsResponse(BaseModel):
    disputes_resolved: int
    flags_handled: int
    total_logs: int

class AuditLogResponse(BaseModel):
    id: int
    action: str
    user_id: int
    target_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
