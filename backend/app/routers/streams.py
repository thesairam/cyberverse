from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.intelligence import LiveStream
from app.schemas.intelligence import LiveStreamOut

router = APIRouter()


@router.get("/", response_model=list[LiveStreamOut])
async def list_streams(
    live_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    q = select(LiveStream)
    if live_only:
        q = q.filter(LiveStream.is_live == True)
    q = q.order_by(LiveStream.is_live.desc(), LiveStream.viewer_count.desc())
    rows = (await db.execute(q)).scalars().all()
    return rows
