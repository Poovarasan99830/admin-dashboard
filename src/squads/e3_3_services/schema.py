from pydantic import BaseModel
from datetime import datetime


class FlaggedBookingOut(BaseModel):
    id: int
    booking_id: int
    reason: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class ProviderOut(BaseModel):
    id: int
    name: str
    status: str
    updated_at: datetime

    class Config:
        orm_mode = True


class AdminActionIn(BaseModel):
    admin_id: int
    reason: str
