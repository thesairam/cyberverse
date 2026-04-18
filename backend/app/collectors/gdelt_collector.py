import asyncio
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote
import httpx
from app.collectors.base import BaseCollector

COUNTRY_COORDS: dict[str, tuple[float, float]] = {
    "United States": (37.09, -95.71), "China": (35.86, 104.19), "Russia": (61.52, 105.32),
    "Germany": (51.16, 10.45), "United Kingdom": (55.37, -3.43), "France": (46.22, 2.21),
    "Japan": (36.20, 138.25), "South Korea": (35.90, 127.76), "India": (20.59, 78.96),
    "Australia": (-25.27, 133.77), "Canada": (56.13, -106.34), "Netherlands": (52.13, 5.29),
    "Norway": (60.47, 8.46), "Sweden": (60.12, 18.64), "Finland": (61.92, 25.74),
    "Denmark": (56.26, 9.50), "Belgium": (50.50, 4.46), "Switzerland": (46.81, 8.22),
    "Austria": (47.51, 14.55), "Spain": (40.46, -3.74), "Italy": (41.87, 12.56),
    "Poland": (51.91, 19.14), "Ukraine": (48.37, 31.16), "Israel": (31.04, 34.85),
    "Iran": (32.42, 53.68), "Turkey": (38.96, 35.24), "Taiwan": (23.69, 120.96),
    "Singapore": (1.35, 103.81), "Malaysia": (4.21, 101.97), "Nigeria": (9.08, 8.67),
    "South Africa": (-30.55, 22.93), "Egypt": (26.82, 30.80), "Saudi Arabia": (23.88, 45.07),
    "UAE": (23.42, 53.84), "Brazil": (-14.23, -51.92), "Mexico": (23.63, -102.55),
    "Cyprus": (35.12, 33.42), "Greece": (39.07, 21.82), "Romania": (45.94, 24.96),
    "Hong Kong": (22.39, 114.10), "Pakistan": (30.37, 69.34), "Indonesia": (-0.78, 113.92),
}

GDELT_DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"
QUERIES = [
    # ── Global / ongoing threats ────────────────────────────────────────────
    ("cybersecurity attack hacker",        ["cybersecurity", "attack"]),
    ("ransomware",                          ["ransomware", "malware"]),
    ("data breach",                         ["data-breach", "privacy"]),
    ("zero day vulnerability exploit",      ["zero-day", "exploit"]),
    ("supply chain attack software",        ["supply-chain", "attack"]),
    ("critical infrastructure cyberattack", ["critical-infrastructure", "attack"]),
    ("DDoS distributed denial service",     ["ddos", "attack"]),
    ("state sponsored cyber espionage",      ["nation-state", "espionage"]),
    # ── AI & Policy ─────────────────────────────────────────────────────────
    ("artificial intelligence regulation",  ["ai", "policy"]),
    ("artificial intelligence cybersecurity",["ai-ethics", "regulation"]),
    # ── NAM / Americas ──────────────────────────────────────────────────────
    ("CISA cybersecurity United States",    ["cisa", "usa", "cybersecurity"]),
    ("Canada cyber attack",                 ["canada", "cybersecurity", "attack"]),
    # ── EMEA / Europe ───────────────────────────────────────────────────────
    ("European cyber attack telecom",       ["europe", "telecom", "attack"]),
    ("Netherlands cybersecurity threat",     ["ncsc", "netherlands", "cybersecurity"]),
    # ── APAC ────────────────────────────────────────────────────────────────
    ("Japan cybersecurity threat",           ["japan", "cybersecurity", "attack"]),
    ("Australia cybersecurity threat",       ["australia", "cybersecurity", "attack"]),
    ("India cyber attack CERT",             ["india", "cybersecurity", "attack"]),
    ("Singapore cyber security",            ["singapore", "cybersecurity"]),
    ("South Korea cyber attack",            ["south-korea", "cybersecurity", "attack"]),
    ("China cyber threat",                  ["china", "apt", "espionage"]),
    # ── Company-specific ────────────────────────────────────────────────────
    ("BasicFit fitness",                    ["basicfit", "fitness", "europe"]),
    ("Basic-Fit gym",                       ["basicfit", "gym", "europe"]),
    ("ASML semiconductor",                  ["asml", "semiconductor", "lithography"]),
    ("ASML cybersecurity compliance",       ["asml", "cybersecurity", "compliance"]),
    ("ASML artificial intelligence chip",   ["asml", "ai", "semiconductor"]),
    ("ASML supply chain technology",        ["asml", "supply-chain", "technology"]),
    ("ASML EUV lithography",                ["asml", "euv", "semiconductor"]),
]


class GDELTCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            for q, tags in QUERIES:
                try:
                    resp = None
                    for attempt in range(3):
                        resp = await client.get(GDELT_DOC_API, params={
                            "query": q, "mode": "artlist", "maxrecords": "50",
                            "timespan": "72h", "sort": "hybridrel", "format": "json",
                        })
                        if resp.status_code == 429:
                            wait = 5 * (2 ** attempt)
                            print(f"[GDELT] Rate limited on {q!r}, retrying in {wait}s (attempt {attempt + 1}/3)")
                            await asyncio.sleep(wait)
                            continue
                        break
                    if resp is None or resp.status_code != 200:
                        continue
                    try:
                        data = resp.json()
                    except Exception:
                        print(f"[GDELT] Non-JSON response for {q!r}")
                        continue
                    for art in (data.get("articles") or []):
                        url = art.get("url", "")
                        title = art.get("title", "")
                        if not url or not title:
                            continue
                        tone = art.get("tone", 0.0) or 0.0
                        date_str = art.get("seendate", "")
                        pub = None
                        try:
                            pub = datetime.strptime(date_str[:14], "%Y%m%dT%H%M%S").replace(tzinfo=timezone.utc)
                        except Exception:
                            pub = datetime.now(timezone.utc)
                        _country = art.get("sourcecountry") or ""
                        _coords = COUNTRY_COORDS.get(_country, (None, None))
                        # Use socialimage excerpt or title as summary fallback
                        _summary = (art.get("title") or "")[:512]
                        results.append({
                            "title": title[:512],
                            "summary": _summary,
                            "source_url": url[:1024],
                            "source_name": art.get("domain", "GDELT")[:128],
                            "event_type": "NEWS",
                            "category_tags": tags,
                            "country": _country or None,
                            "latitude": _coords[0],
                            "longitude": _coords[1],
                            "sentiment_score": round(tone / 10.0, 4),
                            "published_at": pub,
                            "extra": {"gdelt_tone": tone, "gdelt_domain": art.get("domain")},
                        })
                except Exception as exc:
                    print(f"[GDELT] query={q!r} error: {exc}")
                await asyncio.sleep(8)
        return results
