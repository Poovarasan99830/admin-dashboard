from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.admin_flags import FlaggedTransaction
from uuid import UUID
from datetime import datetime

async def list_flagged(db: AsyncSession):
    result = await db.execute(select(FlaggedTransaction))
    return result.scalars().all()

async def resolve_dispute(db: AsyncSession, dispute_id: UUID, resolution: str):
    # For demo: just return resolved info
    return {
        "id": str(dispute_id),
        "status": "resolved",
        "resolved_at": datetime.utcnow().isoformat(),
        "message": resolution,
    }
