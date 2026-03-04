"""Upsert helpers — write collected data to PostgreSQL."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.intelligence import (
    IntelligenceEvent, FinancialSnapshot, LiveStream, ThreatIndicator, CertificationUpdate,
)
from app.sentiment import score_sentiment, score_impact


def _column_names(model) -> set[str]:
    return {c.key for c in inspect(model).mapper.column_attrs}


def _clean(data: dict[str, Any], model) -> dict[str, Any]:
    cols = _column_names(model)
    return {k: v for k, v in data.items() if k in cols}


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def upsert_events(session: AsyncSession, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    enriched = []
    for raw in rows:
        raw.setdefault("sentiment_score", score_sentiment(raw.get("title","") + " " + raw.get("summary","")))
        raw.setdefault("impact_score", score_impact(raw.get("title",""), raw.get("summary",""), raw.get("category_tags",[])))
        raw["updated_at"] = _now()
        enriched.append(_clean(raw, IntelligenceEvent))
    stmt = pg_insert(IntelligenceEvent).values(enriched)
    stmt = stmt.on_conflict_do_update(
        index_elements=["source_url"],
        set_={c: stmt.excluded[c] for c in ("title","summary","sentiment_score","impact_score","updated_at","category_tags","entities_mentioned")},
    )
    await session.execute(stmt)
    await session.commit()
    return len(enriched)


async def upsert_threats(session: AsyncSession, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    cleaned = [_clean(r, ThreatIndicator) for r in rows]
    stmt = pg_insert(ThreatIndicator).values(cleaned)
    stmt = stmt.on_conflict_do_update(
        index_elements=["indicator_id"],
        set_={c: stmt.excluded[c] for c in ("title","description","severity","cvss_score","cvss_vector","affected_products","modified_at")},
    )
    await session.execute(stmt)
    await session.commit()
    return len(cleaned)


async def insert_financial(session: AsyncSession, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    cleaned = [_clean(r, FinancialSnapshot) for r in rows]
    for row in cleaned:
        session.add(FinancialSnapshot(**row))
    await session.commit()
    return len(cleaned)


async def upsert_streams(session: AsyncSession, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    cleaned = [_clean(r, LiveStream) for r in rows]
    stmt = pg_insert(LiveStream).values(cleaned)
    stmt = stmt.on_conflict_do_update(
        index_elements=["video_id"],
        set_={c: stmt.excluded[c] for c in ("title","is_live","viewer_count","thumbnail_url")},
    )
    await session.execute(stmt)
    await session.commit()
    return len(cleaned)


async def upsert_certifications(session: AsyncSession, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    cleaned = [_clean(r, CertificationUpdate) for r in rows]
    for row in cleaned:
        session.add(CertificationUpdate(**row))
    await session.commit()
    return len(cleaned)
