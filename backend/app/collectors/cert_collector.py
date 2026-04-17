import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any
import feedparser
import httpx
from app.collectors.base import BaseCollector

CERT_FEEDS: list[tuple[str, str, str]] = [
    # ── Standards Bodies ────────────────────────────────────────────────────
    ("NIST",             "NIST",         "https://www.nist.gov/blogs/cybersecurity-insights/rss.xml"),
    ("OWASP",            "OWASP",        "https://owasp.org/feed.xml"),
    ("FIRST",            "FIRST",        "https://www.first.org/newsroom/releases/rss.xml"),
    ("SANS ISC",         "SANS",         "https://isc.sans.edu/rssfeed_full.xml"),
    # ── Government CERTs: Americas ──────────────────────────────────────────
    ("CISA",             "CISA",         "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    # ── Government CERTs: Europe ────────────────────────────────────────────
    ("NCSC UK",          "NCSC-UK",      "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"),
    ("NCSC Nederland",   "NCSC-NL",      "https://advisories.ncsc.nl/rss/advisories"),
    ("ENISA",            "ENISA",        "https://www.enisa.europa.eu/publications/rss.xml"),
    ("CERT-FR",          "CERT-FR",      "https://www.cert.ssi.gouv.fr/feed/"),
    # ── Government CERTs: Asia-Pacific ──────────────────────────────────────
    ("JPCERT",           "JPCERT",       "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf"),
    ("ACSC Australia",   "ACSC",         "https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/rss.xml"),
    ("CERT-IN India",    "CERT-IN",      "https://www.cert-in.org.in/RSS.xml"),
    ("KrCERT Korea",     "KrCERT",       "https://www.krcert.or.kr/rss.do"),
]


class CertCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            for source_name, body_name, url in CERT_FEEDS:
                try:
                    content = None
                    for attempt in range(3):
                        resp = await client.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (compatible; CyberVerse/1.0)"
                        })
                        if resp.status_code == 429:
                            wait = 5 * (2 ** attempt)
                            print(f"[Cert] {source_name} rate limited, retry in {wait}s")
                            await asyncio.sleep(wait)
                            continue
                        content = resp.content
                        break
                    if content is None:
                        print(f"[Cert] {source_name} failed after retries (429)")
                        continue
                    feed = feedparser.parse(content)
                    for entry in feed.entries[:10]:
                        pub = None
                        for attr in ("published_parsed", "updated_parsed"):
                            t = getattr(entry, attr, None)
                            if t:
                                pub = datetime(*t[:6], tzinfo=timezone.utc)
                                break
                        link = getattr(entry, "link", "") or ""
                        title = getattr(entry, "title", "") or ""
                        if not title:
                            continue
                        results.append({
                            "body_name": body_name,
                            "standard_id": hashlib.sha256(link.encode()).hexdigest()[:32],
                            "title": title[:512],
                            "summary": (getattr(entry,"summary","") or "")[:2048],
                            "update_type": "announcement",
                            "source_url": link[:1024],
                            "region": "Global",
                            "published_at": pub,
                        })
                except Exception as exc:
                    print(f"[Cert] {source_name} error: {exc}")
                await asyncio.sleep(1)
        return results
