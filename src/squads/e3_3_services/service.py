from sqlalchemy.orm import Session
from src.models import admin_flags, audit_logs
from src.squads.e3_3_services import schema


def get_flagged_bookings(db: Session, status: str | None = None):
    query = db.query(admin_flags.FlaggedBooking)
    if status:
        query = query.filter(admin_flags.FlaggedBooking.status == status)
    return query.all()


def suspend_provider(db: Session, provider_id: int, payload: schema.AdminActionIn):
    provider = db.query(admin_flags.Provider).filter(admin_flags.Provider.id == provider_id).first()
    if not provider:
        return None

    if provider.status != "suspended":
        provider.status = "suspended"
        db.add(provider)

        db.add(audit_logs.AdminAction(
            admin_id=payload.admin_id,
            provider_id=provider.id,
            action="suspend",
            reason=payload.reason,
        ))
        db.commit()
        db.refresh(provider)
    return provider


def restore_provider(db: Session, provider_id: int, payload: schema.AdminActionIn):
    provider = db.query(admin_flags.Provider).filter(admin_flags.Provider.id == provider_id).first()
    if not provider:
        return None

    if provider.status != "active":
        provider.status = "active"
        db.add(provider)

        db.add(audit_logs.AdminAction(
            admin_id=payload.admin_id,
            provider_id=provider.id,
            action="restore",
            reason=payload.reason,
        ))
        db.commit()
        db.refresh(provider)
    return provider
