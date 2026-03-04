from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.intelligence import ThreatIndicator
from app.schemas.intelligence import PaginatedResponse, ThreatIndicatorOut

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ThreatIndicatorOut])
async def list_threats(
    severity: Optional[str] = None,
    indicator_type: Optional[str] = None,
    search: Optional[str] = None,
    min_cvss: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(ThreatIndicator)
    if severity:
        q = q.filter(ThreatIndicator.severity == severity.upper())
    if indicator_type:
        q = q.filter(ThreatIndicator.indicator_type == indicator_type.upper())
    if search:
        q = q.filter(ThreatIndicator.title.ilike(f"%{search}%"))
    if min_cvss is not None:
        q = q.filter(ThreatIndicator.cvss_score >= min_cvss)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one()
    rows = (await db.execute(q.order_by(ThreatIndicator.cvss_score.desc().nullslast()).offset((page-1)*page_size).limit(page_size))).scalars().all()
    return PaginatedResponse(total=total, page=page, page_size=page_size, pages=max(1,(total+page_size-1)//page_size), items=rows)


@router.get("/critical", response_model=list[ThreatIndicatorOut])
async def critical_threats(limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(ThreatIndicator).filter(ThreatIndicator.severity.in_(["CRITICAL","HIGH"]))
        .order_by(ThreatIndicator.cvss_score.desc().nullslast()).limit(limit)
    )).scalars().all()
    return rows
