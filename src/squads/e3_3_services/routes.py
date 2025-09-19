from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.common.database import get_db
from src.squads.e3_3_services import service, schema

router = APIRouter(prefix="/api/v1/admin/services", tags=["Services Oversight"])


@router.get("/flagged", response_model=list[schema.FlaggedBookingOut])
def get_flagged_bookings(status: str | None = None, db: Session = Depends(get_db)):
    return service.get_flagged_bookings(db, status)


@router.post("/providers/{provider_id}/suspend", response_model=schema.ProviderOut)
def suspend_provider(provider_id: int, payload: schema.AdminActionIn, db: Session = Depends(get_db)):
    provider = service.suspend_provider(db, provider_id, payload)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.post("/providers/{provider_id}/restore", response_model=schema.ProviderOut)
def restore_provider(provider_id: int, payload: schema.AdminActionIn, db: Session = Depends(get_db)):
    provider = service.restore_provider(db, provider_id, payload)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider
