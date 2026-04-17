"""
Google News RSS Query Collector — strategy.md "Query Layer" implementation.

Instead of maintaining a fixed source list, this collector continuously
queries Google News RSS for cybersecurity topics, ingests everything
relevant, and lets the normalizer deduplicate + tag downstream.
"""
import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import feedparser
import httpx

from app.collectors.base import BaseCollector

# ── Cybersecurity topic queries (adapted from strategy.md §1) ──────────────
CYBER_QUERIES: list[tuple[str, list[str]]] = [
    # Core threats
    ("cybersecurity breach",                  ["cybersecurity", "breach"]),
    ("ransomware attack",                     ["ransomware", "malware"]),
    ("zero day vulnerability",                ["zero-day", "vulnerability"]),
    ("data breach",                           ["data-breach", "privacy"]),
    ("supply chain cyberattack",              ["supply-chain", "attack"]),
    ("critical infrastructure hack",          ["critical-infrastructure", "attack"]),
    ("DDoS attack",                           ["ddos", "attack"]),
    ("phishing campaign",                     ["phishing", "social-engineering"]),
    # APT / Nation-state
    ("APT nation state cyber espionage",      ["apt", "espionage"]),
    ("state sponsored hacking",               ["nation-state", "hacking"]),
    # Cloud & Enterprise
    ("cloud security breach",                 ["cloud-security", "breach"]),
    ("enterprise cybersecurity",              ["enterprise", "cybersecurity"]),
    # AI & Emerging
    ("AI cybersecurity threat",               ["ai", "cybersecurity"]),
    ("AI regulation policy",                  ["ai", "policy"]),
    # IoT & OT
    ("IoT security vulnerability",            ["iot", "vulnerability"]),
    ("industrial control system attack",      ["ics", "ot-security"]),
    # Privacy & Regulation
    ("data privacy regulation GDPR",          ["privacy", "regulation"]),
    ("cybersecurity policy legislation",      ["policy", "legislation"]),
    # Malware & Exploits
    ("malware trojan backdoor",               ["malware", "trojan"]),
    ("exploit kit vulnerability",             ["exploit", "vulnerability"]),
]

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


class GoogleNewsCollector(BaseCollector):
    """Query-driven collector using Google News RSS search."""

    async def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        async with httpx.AsyncClient(
            timeout=20.0,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CyberVerse/1.0)"},
        ) as client:
            for query, tags in CYBER_QUERIES:
                try:
                    url = f"{GOOGLE_NEWS_RSS}?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
                    content = None
                    for attempt in range(3):
                        resp = await client.get(url)
                        if resp.status_code == 429:
                            wait = 5 * (2 ** attempt)
                            print(f"[GoogleNews] rate limited on '{query}', retry in {wait}s")
                            await asyncio.sleep(wait)
                            continue
                        if resp.status_code >= 400:
                            print(f"[GoogleNews] HTTP {resp.status_code} for '{query}'")
                            break
                        content = resp.content
                        break

                    if content is None:
                        continue

                    feed = feedparser.parse(content)
                    for entry in feed.entries[:15]:
                        link = getattr(entry, "link", "") or ""
                        title = getattr(entry, "title", "") or ""
                        summary = getattr(entry, "summary", "") or ""
                        if not link or not title:
                            continue
                        # Deduplicate within this collection cycle
                        if link in seen_urls:
                            continue
                        seen_urls.add(link)

                        pub = None
                        for attr in ("published_parsed", "updated_parsed"):
                            t = getattr(entry, attr, None)
                            if t:
                                pub = datetime(*t[:6], tzinfo=timezone.utc)
                                break

                        # Extract source name from Google News title suffix
                        source = "Google News"
                        if " - " in title:
                            parts = title.rsplit(" - ", 1)
                            if len(parts) == 2 and len(parts[1]) < 60:
                                source = parts[1].strip()
                                title = parts[0].strip()

                        results.append({
                            "title": title[:512],
                            "summary": summary[:2048],
                            "source_url": link[:1024],
                            "source_name": f"GN:{source}",
                            "event_type": "NEWS",
                            "category_tags": tags,
                            "published_at": pub,
                            "external_id": hashlib.sha256(link.encode()).hexdigest()[:64],
                        })
                except Exception as exc:
                    print(f"[GoogleNews] '{query}' error: {exc}")

                await asyncio.sleep(2)  # polite inter-query delay

        print(f"[GoogleNews] collected {len(results)} articles from {len(CYBER_QUERIES)} queries")
        return results
