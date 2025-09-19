from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.common.database import get_db
from src.squads.e3_1_user_mgmt import service, schema

router = APIRouter(prefix="/admin/users", tags=["Admin User Management"])

@router.get("/", response_model=schema.UserListResponse)
def get_users(status: str = None, name: str = None, email: str = None, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    users, total = service.list_users(db, status, name, email, page, limit)
    return {"users": users, "total": total, "page": page, "limit": limit}

@router.post("/{user_id}/suspend", response_model=schema.ActionResponse)
def suspend(user_id: int, data: schema.ActionRequest, db: Session = Depends(get_db), admin_id: int = 1):
    user = service.suspend_user(db, user_id, admin_id, data)
    return {"message": "User suspended successfully", "user": user}

@router.post("/{user_id}/restore", response_model=schema.ActionResponse)
def restore(user_id: int, data: schema.ActionRequest, db: Session = Depends(get_db), admin_id: int = 1):
    user = service.restore_user(db, user_id, admin_id, data)
    return {"message": "User restored successfully", "user": user}
