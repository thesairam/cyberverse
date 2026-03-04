from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.intelligence import CertificationUpdate
from app.schemas.intelligence import CertificationUpdateOut, PaginatedResponse

router = APIRouter()

TRACKED_BODIES = [
    "NIST","ISO","ENISA","CISA","FIRST","ISC2","ISACA","IETF",
    "ITU-T","OWASP","OECD","UNESCO","IEEE","Partnership on AI","EU AI Act",
    "MITRE","SOC2",
]


@router.get("/", response_model=PaginatedResponse[CertificationUpdateOut])
async def list_certifications(
    body_name: Optional[str] = None,
    region: Optional[str] = None,
    update_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    q = select(CertificationUpdate)
    if body_name:
        q = q.filter(CertificationUpdate.body_name.ilike(f"%{body_name}%"))
    if region:
        q = q.filter(CertificationUpdate.region.ilike(f"%{region}%"))
    if update_type:
        q = q.filter(CertificationUpdate.update_type == update_type.lower())
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one()
    rows = (await db.execute(q.order_by(CertificationUpdate.published_at.desc()).offset((page-1)*page_size).limit(page_size))).scalars().all()
    return PaginatedResponse(total=total, page=page, page_size=page_size, pages=max(1,(total+page_size-1)//page_size), items=rows)


@router.get("/bodies")
async def list_bodies():
    return {"bodies": TRACKED_BODIES}
