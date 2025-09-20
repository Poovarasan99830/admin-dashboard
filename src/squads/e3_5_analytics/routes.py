# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from typing import List
# from src.common.database import get_db
# from src.common.rbac import admin_required
# from src.squads.e3_5_analytics import service, schema

# router = APIRouter(prefix="/api/v1/admin", tags=["Analytics & Logs"])

# @router.get("/analytics", response_model=schema.AnalyticsResponse, dependencies=[Depends(admin_required)])
# def fetch_analytics(db: Session = Depends(get_db)):
#     return service.get_analytics(db)

# @router.get("/audit-logs", response_model=List[schema.AuditLogResponse], dependencies=[Depends(admin_required)])
# def fetch_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return service.get_audit_logs(db, skip=skip, limit=limit)


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.common.database import get_db
from src.common.rbac import admin_required
from src.squads.e3_5_analytics import service, schema

router = APIRouter(tags=["Analytics & Logs"])

@router.get("/analytics", response_model=schema.AnalyticsResponse, dependencies=[Depends(admin_required)])
def fetch_analytics(db: Session = Depends(get_db)):
    return service.get_analytics(db)

@router.get("/audit-logs", response_model=List[schema.AuditLogResponse], dependencies=[Depends(admin_required)])
def fetch_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_audit_logs(db, skip=skip, limit=limit)
