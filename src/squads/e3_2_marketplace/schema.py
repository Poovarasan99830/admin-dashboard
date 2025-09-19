from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FlaggedListingOut(BaseModel):
    id: int
    listing_id: int
    reason: Optional[str]
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True

class ResolveFlagPayload(BaseModel):
    resolved_by: int
    notes: Optional[str] = None

class DisputeOut(BaseModel):
    id: int
    user_id: int
    listing_id: int
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[int] = None
    resolution_notes: Optional[str] = None

    class Config:
        orm_mode = True

class ResolveDisputePayload(BaseModel):
    resolved_by: int
    resolution_notes: Optional[str] = None
