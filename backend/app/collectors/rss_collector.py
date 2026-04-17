import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Any
import feedparser
import httpx
from app.collectors.base import BaseCollector

RSS_FEEDS: list[tuple[str, str, str]] = [
    # ═══════════════════════════════════════════════════════════════════════
    # §1  GLOBAL CYBERSECURITY — Core Sources
    # ═══════════════════════════════════════════════════════════════════════
    ("The Hacker News",       "NEWS",   "https://feeds.feedburner.com/TheHackersNews"),
    ("Dark Reading",          "NEWS",   "https://www.darkreading.com/rss.xml"),
    ("Krebs on Security",     "NEWS",   "https://krebsonsecurity.com/feed/"),
    ("BleepingComputer",      "NEWS",   "https://www.bleepingcomputer.com/feed/"),
    ("SecurityWeek",          "NEWS",   "https://feeds.feedburner.com/securityweek"),
    ("Schneier on Security",  "NEWS",   "https://www.schneier.com/blog/atom.xml"),
    ("CSO Online",            "NEWS",   "https://www.csoonline.com/feed/"),
    ("Infosecurity Mag",      "NEWS",   "https://www.infosecurity-magazine.com/rss/news/"),
    ("Threatpost",            "NEWS",   "https://threatpost.com/feed"),
    ("CyberScoop",            "NEWS",   "https://cyberscoop.com/feed/"),
    ("The Record",            "NEWS",   "https://therecord.media/feed"),
    ("Recorded Future",       "NEWS",   "https://www.recordedfuture.com/feed"),
    ("SC Magazine",           "NEWS",   "https://www.scmagazine.com/home/feed/"),
    ("Hackread",              "NEWS",   "https://www.hackread.com/feed/"),
    ("Security Affairs",      "NEWS",   "https://securityaffairs.com/feed"),

    # ═══════════════════════════════════════════════════════════════════════
    # §2  THREAT INTELLIGENCE & RESEARCH BLOGS
    # ═══════════════════════════════════════════════════════════════════════
    ("Cisco Talos",           "NEWS",   "https://blog.talosintelligence.com/feeds/posts/default"),
    ("Palo Alto Unit 42",     "NEWS",   "https://unit42.paloaltonetworks.com/feed/"),
    ("Google TAG",            "NEWS",   "https://blog.google/threat-analysis-group/rss/"),
    ("Microsoft Security",    "NEWS",   "https://www.microsoft.com/en-us/security/blog/feed/"),
    ("CrowdStrike Blog",      "NEWS",   "https://www.crowdstrike.com/blog/feed/"),
    ("SentinelOne Labs",      "NEWS",   "https://www.sentinelone.com/blog/feed/"),
    ("Kaspersky Securelist",  "NEWS",   "https://securelist.com/feed/"),
    ("Sophos Naked Security", "NEWS",   "https://nakedsecurity.sophos.com/feed/"),
    ("ESET Research",         "NEWS",   "https://www.welivesecurity.com/feed/"),
    ("Rapid7 Blog",           "NEWS",   "https://blog.rapid7.com/rss/"),
    ("Qualys Blog",           "NEWS",   "https://blog.qualys.com/feed"),
    ("CheckPoint Research",   "NEWS",   "https://research.checkpoint.com/feed/"),
    ("Fortinet Blog",         "NEWS",   "https://www.fortinet.com/blog/threat-research.xml"),
    ("Mandiant Blog",         "NEWS",   "https://cloud.google.com/blog/topics/threat-intelligence/rss/"),
    ("Trend Micro Research",  "NEWS",   "https://www.trendmicro.com/en_us/research.html/rss.xml"),
    ("Recorded Future Intel", "NEWS",   "https://therecord.media/feed"),
    ("Proofpoint Blog",       "NEWS",   "https://www.proofpoint.com/us/blog.xml"),
    ("Elastic Security Labs", "NEWS",   "https://www.elastic.co/security-labs/rss/feed.xml"),

    # ═══════════════════════════════════════════════════════════════════════
    # §3  VULNERABILITY / CVE / EXPLOIT FEEDS
    # ═══════════════════════════════════════════════════════════════════════
    ("Zero Day Initiative",   "ALERT",  "https://www.zerodayinitiative.com/rss/published/"),
    ("Exploit-DB",            "ALERT",  "https://www.exploit-db.com/rss.xml"),
    ("Packet Storm",          "ALERT",  "https://packetstormsecurity.com/files/feed/"),
    ("CVE Details",           "ALERT",  "https://www.cvedetails.com/vulnerability-feed.php?vendor_id=0&product_id=0&version_id=0&orderby=1&cvssscoremin=7"),
    ("VulnDB (RiskBased)",   "ALERT",  "https://vuldb.com/?rss.recent"),

    # ═══════════════════════════════════════════════════════════════════════
    # §4  INCIDENT / BREACH / MALWARE TRACKING
    # ═══════════════════════════════════════════════════════════════════════
    ("Troy Hunt (HIBP)",      "NEWS",   "https://www.troyhunt.com/rss/"),
    ("Malwarebytes Labs",     "NEWS",   "https://blog.malwarebytes.com/feed/"),
    ("SANS Internet Storm",   "ALERT",  "https://isc.sans.edu/rssfeed_full.xml"),
    ("Abuse.ch",              "ALERT",  "https://abuse.ch/rss/"),
    ("DataBreaches.net",      "NEWS",   "https://databreaches.net/feed/"),
    ("GrahamCluley",          "NEWS",   "https://grahamcluley.com/feed/"),

    # ═══════════════════════════════════════════════════════════════════════
    # §5  CLOUD / DEVSECOPS / ENTERPRISE SECURITY
    # ═══════════════════════════════════════════════════════════════════════
    ("AWS Security Blog",     "NEWS",   "https://aws.amazon.com/blogs/security/feed/"),
    ("Google Cloud Security", "NEWS",   "https://cloud.google.com/blog/topics/security/rss/"),
    ("Azure Security Blog",   "NEWS",   "https://azure.microsoft.com/en-us/blog/tag/security/feed/"),
    ("Snyk Blog",             "NEWS",   "https://snyk.io/blog/feed/"),

    # ═══════════════════════════════════════════════════════════════════════
    # §6  GOVERNMENT & INSTITUTIONAL ALERTS
    # ═══════════════════════════════════════════════════════════════════════
    ("CISA Alerts",           "ALERT",  "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    ("NCSC UK",               "ALERT",  "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"),
    ("NCSC Nederland",        "ALERT",  "https://advisories.ncsc.nl/rss/advisories"),
    ("CERT-FR",               "ALERT",  "https://www.cert.ssi.gouv.fr/feed/"),
    ("JPCERT",                "ALERT",  "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf"),
    ("NSA Cybersecurity",     "ALERT",  "https://www.nsa.gov/Press-Room/Press-Releases-Statements/rss/"),
    ("FBI Cyber",             "ALERT",  "https://www.fbi.gov/feeds/cyber-news/rss.xml"),
    ("Europol",               "ALERT",  "https://www.europol.europa.eu/rss"),
    ("CERT-IN India",         "ALERT",  "https://www.cert-in.org.in/RSS.xml"),

    # ═══════════════════════════════════════════════════════════════════════
    # §7  COUNTRY / REGIONAL CYBER NEWS
    # ═══════════════════════════════════════════════════════════════════════
    ("The Register Security", "NEWS",   "https://www.theregister.com/security/headlines.atom"),
    ("Heise Security",        "NEWS",   "https://www.heise.de/security/rss/news-atom.xml"),
    ("Qihoo 360 Netlab",      "NEWS",   "https://blog.netlab.360.com/rss/"),
    ("KrCERT",                "ALERT",  "https://www.krcert.or.kr/rss.do"),
    ("Cybersecurity News",    "NEWS",   "https://cybersecuritynews.com/feed/"),

    # ═══════════════════════════════════════════════════════════════════════
    # §8  COMMUNITIES & CURATED FEEDS
    # ═══════════════════════════════════════════════════════════════════════
    ("Reddit r/netsec",       "NEWS",   "https://www.reddit.com/r/netsec/.rss"),
    ("Reddit r/cybersecurity","NEWS",   "https://www.reddit.com/r/cybersecurity/.rss"),
    ("Hacker News",           "NEWS",   "https://hnrss.org/frontpage"),
    ("Risky.Biz Newsletter",  "NEWS",   "https://risky.biz/feeds/risky-business/"),
    ("SANS NewsBites",        "NEWS",   "https://www.sans.org/newsletters/newsbites/rss"),

    # ═══════════════════════════════════════════════════════════════════════
    # §9  AI & TECH (Cross-cutting)
    # ═══════════════════════════════════════════════════════════════════════
    ("TechCrunch AI",         "NEWS",   "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI",        "NEWS",   "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review",       "NEWS",   "https://www.technologyreview.com/feed/"),
    ("Wired Security",        "NEWS",   "https://www.wired.com/feed/category/security/latest/rss"),
    ("BBC Technology",        "NEWS",   "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("ZDNet Security",        "NEWS",   "https://www.zdnet.com/topic/security/rss.xml"),
    ("The Verge Security",    "NEWS",   "https://www.theverge.com/rss/cyber-security/index.xml"),
    ("Ars Technica Security", "NEWS",   "https://feeds.arstechnica.com/arstechnica/security"),

    # ═══════════════════════════════════════════════════════════════════════
    # §10  POLICY & STANDARDS
    # ═══════════════════════════════════════════════════════════════════════
    ("NIST",                  "POLICY", "https://www.nist.gov/news-events/news/rss.xml"),
    ("AI Now Institute",      "POLICY", "https://ainowinstitute.org/feed"),
    ("EFF Deeplinks",         "POLICY", "https://www.eff.org/rss/updates.xml"),
    ("Lawfare",               "POLICY", "https://www.lawfaremedia.org/feed"),
]

_TYPE_MAP = {src: etype for src, etype, _ in RSS_FEEDS}


class RSSCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
            for source_name, event_type, url in RSS_FEEDS:
                try:
                    content = None
                    for attempt in range(3):
                        resp = await client.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (compatible; CyberVerse/1.0)"
                        })
                        if resp.status_code == 429:
                            wait = 5 * (2 ** attempt)
                            print(f"[RSS] {source_name} rate limited, retry in {wait}s")
                            await asyncio.sleep(wait)
                            continue
                        content = resp.content
                        break
                    if content is None:
                        print(f"[RSS] {source_name} failed after retries (429)")
                        continue
                    feed = feedparser.parse(content)
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
                await asyncio.sleep(1)  # polite delay between feeds
        return results
