from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.intelligence import FinancialSnapshot
from app.schemas.intelligence import FinancialSnapshotOut

router = APIRouter()


@router.get("/", response_model=list[FinancialSnapshotOut])
async def list_snapshots(sector: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    # Latest snapshot per ticker
    subq = (select(FinancialSnapshot.ticker, func.max(FinancialSnapshot.snapshot_at).label("latest"))
            .group_by(FinancialSnapshot.ticker).subquery())
    q = select(FinancialSnapshot).join(subq, (FinancialSnapshot.ticker == subq.c.ticker) &
        (FinancialSnapshot.snapshot_at == subq.c.latest))
    if sector:
        q = q.filter(FinancialSnapshot.sector == sector.lower())
    rows = (await db.execute(q)).scalars().all()
    return rows


@router.get("/movers", response_model=dict)
async def movers(db: AsyncSession = Depends(get_db)):
    subq = (select(FinancialSnapshot.ticker, func.max(FinancialSnapshot.snapshot_at).label("latest"))
            .group_by(FinancialSnapshot.ticker).subquery())
    q = (select(FinancialSnapshot).join(subq, (FinancialSnapshot.ticker == subq.c.ticker) &
        (FinancialSnapshot.snapshot_at == subq.c.latest))
        .filter(FinancialSnapshot.change_pct != None))
    rows = (await db.execute(q)).scalars().all()
    sorted_rows = sorted(rows, key=lambda r: r.change_pct or 0, reverse=True)
    return {
        "gainers": [FinancialSnapshotOut.model_validate(r) for r in sorted_rows[:5]],
        "losers":  [FinancialSnapshotOut.model_validate(r) for r in sorted_rows[-5:]],
    }


@router.get("/{ticker}/history", response_model=list[FinancialSnapshotOut])
async def ticker_history(ticker: str, limit: int = Query(30, ge=1, le=200), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(FinancialSnapshot).filter(FinancialSnapshot.ticker == ticker.upper())
        .order_by(FinancialSnapshot.snapshot_at.desc()).limit(limit)
    )).scalars().all()
    return rows
