from pydantic import BaseModel
from datetime import datetime

# Request/Response Models

class UserBase(BaseModel):
    name: str
    email: str

class UserResponse(UserBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SuspendRestoreRequest(BaseModel):
    reason: str | None = None

class AdminActionResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    target_user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
