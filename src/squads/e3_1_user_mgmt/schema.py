from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    id: int
    name: str
    email: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserListResponse(BaseModel):
    users: List[UserBase]
    total: int
    page: int
    limit: int

class ActionRequest(BaseModel):   # ✅ This should exist
    reason: Optional[str] = None

class ActionResponse(BaseModel):
    message: str
    user: UserBase








