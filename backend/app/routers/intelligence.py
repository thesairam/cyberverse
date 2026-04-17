from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.intelligence import IntelligenceEvent
from app.schemas.intelligence import IntelligenceEventOut, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[IntelligenceEventOut])
async def list_events(
    event_type: Optional[str] = None,
    country: Optional[str] = None,
    source_name: Optional[str] = None,
    search: Optional[str] = None,
    min_impact: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(IntelligenceEvent)
    if event_type:
        q = q.filter(IntelligenceEvent.event_type == event_type.upper())
    if country:
        q = q.filter(IntelligenceEvent.country.ilike(f"%{country}%"))
    if source_name:
        q = q.filter(IntelligenceEvent.source_name.ilike(f"%{source_name}%"))
    if search:
        q = q.filter(
            (IntelligenceEvent.title.ilike(f"%{search}%")) |
            (IntelligenceEvent.summary.ilike(f"%{search}%")) |
            (IntelligenceEvent.source_name.ilike(f"%{search}%"))
        )
    if min_impact is not None:
        q = q.filter(IntelligenceEvent.impact_score >= min_impact)
    total_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(total_q)).scalar_one()
    rows = (await db.execute(q.order_by(IntelligenceEvent.published_at.desc()).offset((page-1)*page_size).limit(page_size))).scalars().all()
    return PaginatedResponse(total=total, page=page, page_size=page_size, pages=max(1,(total+page_size-1)//page_size), items=rows)


@router.get("/top", response_model=list[IntelligenceEventOut])
async def top_events(n: int = Query(10, ge=1, le=50), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(IntelligenceEvent).order_by(IntelligenceEvent.impact_score.desc()).limit(n))).scalars().all()
    return rows


@router.get("/map", response_model=list[IntelligenceEventOut])
async def map_events(
    event_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(IntelligenceEvent).filter(
        IntelligenceEvent.latitude != None,
        IntelligenceEvent.longitude != None,
    )
    if event_type:
        q = q.filter(IntelligenceEvent.event_type == event_type.upper())
    rows = (await db.execute(q.order_by(IntelligenceEvent.published_at.desc()).limit(500))).scalars().all()
    return rows


@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    by_type = (await db.execute(
        select(IntelligenceEvent.event_type, func.count()).group_by(IntelligenceEvent.event_type)
    )).all()
    by_country = (await db.execute(
        select(IntelligenceEvent.country, func.count()).filter(IntelligenceEvent.country != None)
        .group_by(IntelligenceEvent.country).order_by(func.count().desc()).limit(20)
    )).all()
    total = (await db.execute(select(func.count()).select_from(IntelligenceEvent))).scalar_one()
    return {
        "total": total,
        "by_type": {t: c for t, c in by_type},
        "top_countries": {c: n for c, n in by_country},
    }


@router.get("/sources")
async def list_sources(db: AsyncSession = Depends(get_db)):
    """Return distinct source names with article counts."""
    rows = (await db.execute(
        select(IntelligenceEvent.source_name, func.count())
        .group_by(IntelligenceEvent.source_name)
        .order_by(func.count().desc())
    )).all()
    return {"sources": [{"name": n, "count": c} for n, c in rows]}
