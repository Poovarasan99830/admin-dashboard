from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.disputes import User
from src.models.admin_flags import AdminAction
from src.squads.e3_1_user_mgmt.schema import ActionRequest

def list_users(db: Session, status_filter: str = None, name: str = None, email: str = None, page: int = 1, limit: int = 10):
    query = db.query(User)

    if status_filter:
        query = query.filter(User.status == status_filter)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    total = query.count()
    users = query.offset((page - 1) * limit).limit(limit).all()

    return users, total

def suspend_user(db: Session, user_id: int, admin_id: int, data: ActionRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status == "suspended":
        raise HTTPException(status_code=409, detail="User already suspended")

    user.status = "suspended"
    db.add(user)

    log = AdminAction(admin_id=admin_id, action="suspend", target_user_id=user.id, reason=data.reason)
    db.add(log)
    db.commit()
    db.refresh(user)

    return user

def restore_user(db: Session, user_id: int, admin_id: int, data: ActionRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status == "active":
        raise HTTPException(status_code=409, detail="User already active")

    user.status = "active"
    db.add(user)

    log = AdminAction(admin_id=admin_id, action="restore", target_user_id=user.id, reason=data.reason)
    db.add(log)
    db.commit()
    db.refresh(user)

    return user
