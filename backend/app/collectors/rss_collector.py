import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any
import feedparser
from app.collectors.base import BaseCollector

RSS_FEEDS: list[tuple[str, str, str]] = [
    # (source_name, event_type, url)
    ("The Hacker News",      "NEWS",        "https://feeds.feedburner.com/TheHackersNews"),
    ("Dark Reading",         "NEWS",        "https://www.darkreading.com/rss.xml"),
    ("Bleeping Computer",    "NEWS",        "https://www.bleepingcomputer.com/feed/"),
    ("Krebs on Security",    "NEWS",        "https://krebsonsecurity.com/feed/"),
    ("CyberScoop",           "NEWS",        "https://cyberscoop.com/feed/"),
    ("SC Magazine",          "NEWS",        "https://www.scmagazine.com/feed"),
    ("Security Week",        "NEWS",        "https://feeds.feedburner.com/securityweek"),
    ("CISA Alerts",          "ALERT",       "https://www.cisa.gov/uscert/ncas/all.xml"),
    ("NVD CVE",              "ALERT",       "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml"),
    ("TechCrunch AI",        "NEWS",        "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI",       "NEWS",        "https://venturebeat.com/category/ai/feed/"),
    ("Wired Security",       "NEWS",        "https://www.wired.com/feed/category/security/latest/rss"),
    ("MIT Tech Review",      "NEWS",        "https://www.technologyreview.com/feed/"),
    ("BBC Technology",       "NEWS",        "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("Reuters Technology",   "NEWS",        "https://feeds.reuters.com/reuters/technologyNews"),
    ("NIST",                 "POLICY",      "https://www.nist.gov/news-events/cybersecurity/rss.xml"),
    ("ENISA",                "POLICY",      "https://www.enisa.europa.eu/media/news-items/news-wires/RSS"),
    ("AI Now Institute",     "POLICY",      "https://ainowinstitute.org/feed"),
    ("Hacker News",          "NEWS",        "https://hnrss.org/frontpage"),
    ("SANS Internet Storm",  "ALERT",       "https://isc.sans.edu/rssfeed_full.xml"),
    # European & global coverage
    ("The Record",           "NEWS",        "https://therecord.media/feed/rss"),
    ("Security Affairs",     "NEWS",        "https://securityaffairs.com/feed"),
    ("ZDNet Security",       "NEWS",        "https://www.zdnet.com/topic/security/rss.xml"),
    ("Threatpost",           "NEWS",        "https://threatpost.com/feed"),
    ("DataBreaches.net",     "NEWS",        "https://www.databreaches.net/feed"),
    # Dutch / EU institutional
    ("NCSC Nederland",       "ALERT",       "https://www.ncsc.nl/actueel/rss/actueel.rss"),
    ("Security.NL",          "NEWS",        "https://feeds.security.nl/rss/news"),
    ("ENISA News",           "POLICY",      "https://www.enisa.europa.eu/news/enisa-news/RSS"),
    ("EU-CERT",              "ALERT",       "https://cert.europa.eu/static/WhitePapers/CERT-EU-SWP_FEED.xml"),
    # Broader attack coverage
    ("Recorded Future",      "NEWS",        "https://www.recordedfuture.com/feed"),
    ("Cybersecurity News",   "NEWS",        "https://cybersecuritynews.com/feed/"),
    ("Infosecurity Mag",     "NEWS",        "https://www.infosecurity-magazine.com/rss/news/"),
    ("CSO Online",           "NEWS",        "https://www.csoonline.com/index.rss"),
]

_TYPE_MAP = {src: etype for src, etype, _ in RSS_FEEDS}


class RSSCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        results: list[dict[str, Any]] = []
        for source_name, event_type, url in RSS_FEEDS:
            try:
                feed = await loop.run_in_executor(None, feedparser.parse, url)
                for entry in feed.entries[:20]:
                    pub = None
                    for attr in ("published_parsed", "updated_parsed"):
                        t = getattr(entry, attr, None)
                        if t:
                            pub = datetime(*t[:6], tzinfo=timezone.utc)
                            break
                    link = getattr(entry, "link", "") or ""
                    title = getattr(entry, "title", "") or ""
                    summary = getattr(entry, "summary", "") or ""
                    if not link or not title:
                        continue
                    results.append({
                        "title": title[:512],
                        "summary": summary[:2048],
                        "source_url": link[:1024],
                        "source_name": source_name,
                        "event_type": event_type,
                        "published_at": pub,
                        "external_id": hashlib.sha256(link.encode()).hexdigest()[:64],
                    })
            except Exception as exc:
                print(f"[RSS] {source_name} error: {exc}")
        return results
