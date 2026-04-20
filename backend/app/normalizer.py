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


_COUNTRY_COORDS: dict[str, tuple[float, float]] = {
    "United States": (37.09, -95.71), "United Kingdom": (55.37, -3.43),
    "European Union": (50.85, 4.35), "Germany": (51.16, 10.45),
    "France": (46.22, 2.21), "Netherlands": (52.13, 5.29),
    "Russia": (61.52, 105.32), "China": (35.86, 104.19),
    "Japan": (36.20, 138.25), "Australia": (-25.27, 133.77),
    "India": (20.59, 78.96), "South Korea": (35.90, 127.76),
    "Israel": (31.04, 34.85), "Iran": (32.42, 53.68),
    "North Korea": (40.34, 127.51), "Canada": (56.13, -106.34),
    "Singapore": (1.35, 103.81), "Brazil": (-14.23, -51.92),
    "Taiwan": (23.69, 120.96), "Ukraine": (48.37, 31.16),
    "Turkey": (38.96, 35.24), "Saudi Arabia": (23.88, 45.07),
    "UAE": (23.42, 53.84), "South Africa": (-30.55, 22.93),
    "Nigeria": (9.08, 8.67), "Mexico": (23.63, -102.55),
    "Poland": (51.91, 19.14), "Italy": (41.87, 12.56),
    "Spain": (40.46, -3.74), "Switzerland": (46.81, 8.22),
    "Sweden": (60.12, 18.64), "Norway": (60.47, 8.46),
    "Finland": (61.92, 25.74), "Denmark": (56.26, 9.50),
    "Belgium": (50.50, 4.46), "Austria": (47.51, 14.55),
    "Romania": (45.94, 24.96), "Greece": (39.07, 21.82),
    "Indonesia": (-0.78, 113.92), "Malaysia": (4.21, 101.97),
    "Pakistan": (30.37, 69.34), "Egypt": (26.82, 30.80),
    "Hong Kong": (22.39, 114.10), "Cyprus": (35.12, 33.42),
    "Philippines": (12.88, 121.77), "Thailand": (15.87, 100.99),
    "Bangladesh": (23.68, 90.35), "New Zealand": (-40.90, 174.89),
    "Czech Republic": (49.82, 15.47), "Sri Lanka": (7.87, 80.77),
    "Malta": (35.94, 14.37), "Azerbaijan": (40.14, 47.57),
    "Morocco": (31.79, -7.09), "Chile": (-35.68, -71.54),
    "Kenya": (0.02, 37.91), "Ghana": (7.95, -1.02),
    "Myanmar": (21.91, 95.96), "Syria": (34.80, 38.99),
    "Jamaica": (18.11, -77.29), "Bahamas": (25.03, -77.39),
    "Bosnia-Herzegovina": (43.92, 17.68), "Madagascar": (-18.77, 46.87),
    "Colombia": (4.57, -74.30), "Argentina": (-38.42, -63.62),
    "Peru": (-9.19, -75.02), "Vietnam": (14.06, 108.28),
    "Cambodia": (12.57, 104.99), "Nepal": (28.39, 84.12),
    "Iraq": (33.22, 43.68), "Jordan": (30.59, 36.24),
    "Lebanon": (33.85, 35.86), "Qatar": (25.35, 51.18),
    "Kuwait": (29.31, 47.48), "Oman": (21.47, 55.98),
    "Ethiopia": (9.14, 40.49), "Tanzania": (-6.37, 34.89),
    "Uganda": (1.37, 32.29), "Mozambique": (-18.67, 35.53),
}


def _detect_country(title: str, summary: str, source_name: str) -> str | None:
    """Detect country/region from content keywords."""
    combined = (title + " " + (summary or "") + " " + (source_name or "")).lower()
    for region, keywords in _REGION_KEYWORDS.items():
        if any(kw in combined for kw in keywords):
            return region
    return None


def _geo_coords(country: str | None) -> tuple[float | None, float | None]:
    """Look up lat/lng for a detected country name."""
    if country and country in _COUNTRY_COORDS:
        return _COUNTRY_COORDS[country]
    return (None, None)


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
        # Geo-coordinate lookup for map integration
        if raw.get("country") and not raw.get("latitude"):
            lat, lng = _geo_coords(raw["country"])
            raw["latitude"] = lat
            raw["longitude"] = lng

        raw.setdefault("sentiment_score", score_sentiment(title + " " + summary))
        raw.setdefault("impact_score", score_impact(title, summary, raw.get("category_tags", [])))
        raw["updated_at"] = _now()
        enriched.append(_clean(raw, IntelligenceEvent))
    # pg_insert multi-values requires every dict to expose the same keys —
    # otherwise SQLAlchemy raises CompileError on the missing column's bindparam.
    all_keys: set[str] = set()
    for r in enriched:
        all_keys |= r.keys()
    for r in enriched:
        for k in all_keys:
            r.setdefault(k, None)
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
