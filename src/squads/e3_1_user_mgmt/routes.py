from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schema, service
from app.database import get_db

router = APIRouter(prefix="/api/v1/admin/users", tags=["User Management"])

# 1. List Users
@router.get("/", response_model=list[schema.UserResponse])
def list_users(status: str = None, email: str = None, name: str = None, db: Session = Depends(get_db)):
    return service.get_users(db, status, email, name)

# 2. Suspend User
@router.post("/{user_id}/suspend", response_model=schema.UserResponse)
def suspend_user(user_id: int, request: schema.SuspendRestoreRequest, db: Session = Depends(get_db)):
    user = service.suspend_user(db, user_id, admin_id=1, reason=request.reason)  # mock admin_id=1
    if not user:
        raise HTTPException(status_code=409, detail="User not found or already suspended")
    return user

# 3. Restore User
@router.post("/{user_id}/restore", response_model=schema.UserResponse)
def restore_user(user_id: int, request: schema.SuspendRestoreRequest, db: Session = Depends(get_db)):
    user = service.restore_user(db, user_id, admin_id=1, reason=request.reason)  # mock admin_id=1
    if not user:
        raise HTTPException(status_code=409, detail="User not found or already active")
    return user
