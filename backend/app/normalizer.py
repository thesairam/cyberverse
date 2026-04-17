"""Upsert helpers — write collected data to PostgreSQL."""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.intelligence import (
    IntelligenceEvent, FinancialSnapshot, LiveStream, ThreatIndicator, CertificationUpdate,
)
from app.sentiment import score_sentiment, score_impact


# ── Strategy §5: Tagging & Categorization ──────────────────────────────────
_DOMAIN_TAGS: dict[str, list[str]] = {
    "malware":           ["malware", "trojan", "backdoor", "worm", "botnet", "spyware", "adware", "rootkit", "keylogger"],
    "ransomware":        ["ransomware", "ransom", "lockbit", "conti", "revil", "blackcat", "alphv"],
    "vulnerability":     ["vulnerability", "cve-", "zero-day", "zero day", "0-day", "exploit", "patch", "buffer overflow"],
    "data-breach":       ["data breach", "breach", "leaked", "compromised", "stolen data", "exfiltrat"],
    "phishing":          ["phishing", "spear-phishing", "social engineering", "credential theft", "bec"],
    "apt":               ["apt", "nation-state", "state-sponsored", "advanced persistent", "espionage", "cyber espionage"],
    "ddos":              ["ddos", "distributed denial", "denial of service", "dos attack"],
    "cloud-security":    ["cloud security", "aws", "azure", "gcp", "s3 bucket", "cloud breach", "misconfigur"],
    "iot-security":      ["iot", "internet of things", "smart device", "embedded", "firmware"],
    "ics-ot":            ["scada", "ics", "industrial control", "operational technology", "plc", "ot security"],
    "supply-chain":      ["supply chain", "solarwinds", "dependency", "package", "npm", "pypi"],
    "privacy":           ["privacy", "gdpr", "ccpa", "data protection", "surveillance", "tracking"],
    "policy":            ["regulation", "legislation", "compliance", "sanctions", "executive order", "policy"],
    "ai-security":       ["artificial intelligence", "machine learning", "llm", "generative ai", "deepfake", "ai security"],
    "crypto-security":   ["cryptocurrency", "blockchain", "crypto theft", "wallet", "defi", "web3"],
    "identity":          ["authentication", "mfa", "identity", "credential", "password", "sso", "oauth"],
}

_REGION_KEYWORDS: dict[str, list[str]] = {
    "United States":   ["united states", "usa", "us-cert", "cisa", "fbi", "nsa", "american"],
    "United Kingdom":  ["united kingdom", "uk", "ncsc", "british", "gchq"],
    "European Union":  ["european union", "eu", "enisa", "europol", "gdpr"],
    "Germany":         ["germany", "german", "bsi", "heise"],
    "France":          ["france", "french", "anssi", "cert-fr"],
    "Netherlands":     ["netherlands", "dutch", "ncsc-nl"],
    "Russia":          ["russia", "russian", "apt28", "apt29", "fancy bear", "cozy bear"],
    "China":           ["china", "chinese", "apt41", "apt10", "panda"],
    "Japan":           ["japan", "japanese", "jpcert"],
    "Australia":       ["australia", "australian", "acsc", "asd"],
    "India":           ["india", "indian", "cert-in"],
    "South Korea":     ["south korea", "korean", "krcert"],
    "Israel":          ["israel", "israeli", "unit 8200"],
    "Iran":            ["iran", "iranian", "apt33", "apt35"],
    "North Korea":     ["north korea", "lazarus", "kimsuky"],
    "Canada":          ["canada", "canadian", "cccs"],
    "Singapore":       ["singapore", "csa"],
    "Brazil":          ["brazil", "brazilian"],
}


def _auto_tags(title: str, summary: str, existing_tags: list[str] | None = None) -> list[str]:
    """Assign domain + region tags based on keyword matching (strategy §5)."""
    tags = list(existing_tags or [])
    combined = (title + " " + (summary or "")).lower()
    for domain, keywords in _DOMAIN_TAGS.items():
        if domain not in tags and any(kw in combined for kw in keywords):
            tags.append(domain)
    return tags[:12]  # cap to avoid bloat


def _detect_country(title: str, summary: str, source_name: str) -> str | None:
    """Detect country/region from content keywords."""
    combined = (title + " " + (summary or "") + " " + (source_name or "")).lower()
    for region, keywords in _REGION_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            return region
    return None


def _title_hash(title: str) -> str:
    """Normalized title hash for deduplication (strategy §3)."""
    normalized = "".join(c for c in title.lower() if c.isalnum() or c == " ").strip()
    return hashlib.sha256(normalized.encode()).hexdigest()[:32]


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
    seen_title_hashes: set[str] = set()
    for raw in rows:
        # Strategy §3: title-based deduplication within batch
        th = _title_hash(raw.get("title", ""))
        if th in seen_title_hashes:
            continue
        seen_title_hashes.add(th)

        title = raw.get("title", "")
        summary = raw.get("summary", "")
        source_name = raw.get("source_name", "")

        # Strategy §5: auto-tagging
        raw["category_tags"] = _auto_tags(title, summary, raw.get("category_tags"))
        # Strategy §5: geography detection
        if not raw.get("country"):
            raw["country"] = _detect_country(title, summary, source_name)

        raw.setdefault("sentiment_score", score_sentiment(title + " " + summary))
        raw.setdefault("impact_score", score_impact(title, summary, raw.get("category_tags", [])))
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
