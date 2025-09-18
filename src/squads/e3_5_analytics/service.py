from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database import get_db
from src.squads.e3_4_payments import service, schema
from uuid import UUID

router = APIRouter(prefix="/admin/payments", tags=["Payments"])

@router.get("/flagged", response_model=list[schema.FlaggedOut])
async def get_flagged_transactions(db: AsyncSession = Depends(get_db)):
    flagged = await service.list_flagged(db)
    if not flagged:
        raise HTTPException(status_code=404, detail="No flagged transactions found")
    return flagged

@router.post("/disputes/{dispute_id}/resolve")
async def resolve_dispute(dispute_id: UUID, body: schema.DisputeResolution, db: AsyncSession = Depends(get_db)):
    result = await service.resolve_dispute(db, dispute_id, body.resolution)
    return result
