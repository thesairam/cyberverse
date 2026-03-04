import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any
import feedparser
from app.collectors.base import BaseCollector

CERT_FEEDS: list[tuple[str, str, str]] = [
    ("NIST",             "NIST",         "https://www.nist.gov/blogs/cybersecurity-insights/rss.xml"),
    ("ENISA",            "ENISA",        "https://www.enisa.europa.eu/media/news-items/news-wires/RSS"),
    ("CISA",             "CISA",         "https://www.cisa.gov/uscert/ncas/all.xml"),
    ("ISC2",             "ISC2",         "https://www.isc2.org/rss/News"),
    ("ISACA",            "ISACA",        "https://www.isaca.org/resources/news-and-trends/newsletters/atisaca-rss-feed"),
    ("OWASP",            "OWASP",        "https://owasp.org/feed.xml"),
    ("IEEE Security",    "IEEE",         "https://ieeexplore.ieee.org/rss/TOC8013.XML"),
    ("OECD AI",          "OECD",         "https://www.oecd.org/digital/artificial-intelligence/ai-news.xml"),
    ("FIRST",            "FIRST",        "https://www.first.org/newsroom/releases/rss.xml"),
]


class CertCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        results: list[dict[str, Any]] = []
        for source_name, body_name, url in CERT_FEEDS:
            try:
                feed = await loop.run_in_executor(None, feedparser.parse, url)
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
        return results
