from fastapi import APIRouter, Depends, Query, Path, status
from typing import List, Optional
from sqlalchemy.orm import Session
from src.common.database import get_db
from src.common.rbac import admin_required
from src.squads.e3_2_marketplace import service, schema
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/admin/marketplace", tags=["admin.marketplace"])

@router.get("/flagged", response_model=List[schema.FlaggedListingOut])
def list_flagged(
    status: Optional[str] = Query(None, description="Filter by status: pending, reviewed, resolved"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _admin = Depends(admin_required),
):
    results = service.get_flagged_listings(db=db, status=status, limit=limit, offset=offset)
    return results

@router.post("/flagged/{flag_id}/resolve", response_model=schema.FlaggedListingOut)
def resolve_flag(flag_id: int = Path(..., gt=0), payload: schema.ResolveFlagPayload = None, db: Session = Depends(get_db), _admin = Depends(admin_required)):
    payload = payload or schema.ResolveFlagPayload(resolved_by=_admin["user_id"])
    flag = service.resolve_flag(db=db, flag_id=flag_id, resolved_by=payload.resolved_by, notes=payload.notes)
    return flag

@router.post("/disputes/{dispute_id}/resolve", response_model=schema.DisputeOut)
def resolve_dispute(dispute_id: int = Path(..., gt=0), payload: schema.ResolveDisputePayload = None, db: Session = Depends(get_db), _admin = Depends(admin_required)):
    payload = payload or schema.ResolveDisputePayload(resolved_by=_admin["user_id"])
    dispute = service.resolve_dispute(db=db, dispute_id=dispute_id, resolved_by=payload.resolved_by, resolution_notes=payload.resolution_notes)
    return dispute
