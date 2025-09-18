from sqlalchemy.orm import Session
from app import models

# List users with filters
def get_users(db: Session, status=None, email=None, name=None):
    query = db.query(models.User)
    if status:
        query = query.filter(models.User.status == status)
    if email:
        query = query.filter(models.User.email.ilike(f"%{email}%"))
    if name:
        query = query.filter(models.User.name.ilike(f"%{name}%"))
    return query.all()

# Suspend user
def suspend_user(db: Session, user_id: int, admin_id: int, reason: str = None):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.status == "active").first()
    if not user:
        return None
    user.status = "suspended"

    action = models.AdminAction(
        admin_id=admin_id,
        action="suspend",
        target_user_id=user_id
    )
    db.add(action)
    db.commit()
    db.refresh(user)
    return user

# Restore user
def restore_user(db: Session, user_id: int, admin_id: int, reason: str = None):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.status == "suspended").first()
    if not user:
        return None
    user.status = "active"

    action = models.AdminAction(
        admin_id=admin_id,
        action="restore",
        target_user_id=user_id
    )
    db.add(action)
    db.commit()
    db.refresh(user)
    return user
