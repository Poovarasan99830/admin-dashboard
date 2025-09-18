from sqlalchemy.orm import Session
from src.models.audit_logs import AuditLog
from src.squads.e3_5_analytics.schema import AnalyticsResponse
from sqlalchemy import func

def get_analytics(db: Session) -> AnalyticsResponse:
    disputes_resolved = db.query(AuditLog).filter(AuditLog.action == "dispute_resolved").count()
    flags_handled = db.query(AuditLog).filter(AuditLog.action == "flag_handled").count()
    total_logs = db.query(func.count(AuditLog.id)).scalar()
    return AnalyticsResponse(
        disputes_resolved=disputes_resolved,
        flags_handled=flags_handled,
        total_logs=total_logs,
    )

def get_audit_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AuditLog).offset(skip).limit(limit).all()
