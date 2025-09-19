from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.models.flagged_listings import FlaggedListing, FlagStatus
from src.models.disputes import Dispute, DisputeStatus
from src.common.events import send_notification
from src.common.exceptions import not_found, conflict
from sqlalchemy import select, update

def get_flagged_listings(db: Session, status: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[FlaggedListing]:
    q = select(FlaggedListing)
    if status:
        try:
            _ = FlagStatus(status)
            q = q.where(FlaggedListing.status == status)
        except Exception:
            # unknown status => return empty
            return []
    q = q.limit(limit).offset(offset)
    result = db.execute(q).scalars().all()
    return result

def resolve_flag(db: Session, flag_id: int, resolved_by: int, notes: Optional[str] = None) -> FlaggedListing:
    flag = db.get(FlaggedListing, flag_id)
    if not flag:
        not_found("Flagged listing not found")
    if flag.status == FlagStatus.resolved:
        conflict("Flag already resolved")
    flag.status = FlagStatus.resolved
    flag.resolved_at = datetime.utcnow()
    flag.resolved_by = resolved_by
    if notes:
        flag.notes = notes
    db.add(flag)
    db.commit()
    db.refresh(flag)
    # TODO: notify listing owner and reporter (requires user/listing service)
    # send_notification(...)
    return flag

def resolve_dispute(db: Session, dispute_id: int, resolved_by: int, resolution_notes: Optional[str] = None) -> Dispute:
    dispute = db.get(Dispute, dispute_id)
    if not dispute:
        not_found("Dispute not found")
    if dispute.status == DisputeStatus.resolved:
        conflict("Dispute already resolved")
    dispute.status = DisputeStatus.resolved
    dispute.resolved_at = datetime.utcnow()
    dispute.resolved_by = resolved_by
    if resolution_notes:
        dispute.resolution_notes = resolution_notes
    db.add(dispute)
    db.commit()
    db.refresh(dispute)

    # Notify buyer/seller (placeholder)
    send_notification(dispute.user_id, "Dispute resolved", resolution_notes or "Admin resolved dispute")
    return dispute
