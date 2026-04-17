# CyberVerse — Comprehensive Testing Plan

> **Goal:** Verify every component, data source, and feature for **authenticity** (real, trustworthy data), **accuracy** (correct processing, scoring, rendering), and **diversity** (broad geographic/topical/sector coverage).

---

## Table of Contents

1. [Data Source Authenticity](#1-data-source-authenticity)
2. [Collector Accuracy](#2-collector-accuracy)
3. [Normalizer & Sentiment Pipeline](#3-normalizer--sentiment-pipeline)
4. [Database Integrity](#4-database-integrity)
5. [API Endpoint Accuracy](#5-api-endpoint-accuracy)
6. [Frontend Rendering & UX](#6-frontend-rendering--ux)
7. [Infrastructure & Deployment](#7-infrastructure--deployment)
8. [Diversity & Coverage Audit](#8-diversity--coverage-audit)
9. [End-to-End Scenarios](#9-end-to-end-scenarios)

---

## 1. Data Source Authenticity

Verify every feed URL is reachable, returns valid data, and originates from a legitimate organization.

### 1.1 RSS Feeds (79 feeds)

| # | Source | URL | Auth Check | Content Check |
|---|---|---|---|---|
| 1 | The Hacker News | `feeds.feedburner.com/TheHackersNews` | ☐ HTTP 200, valid XML | ☐ Entries have `<title>`, `<link>`, `<pubDate>` |
| 2 | Dark Reading | `darkreading.com/rss.xml` | ☐ HTTP 200, valid XML | ☐ Cybersecurity-relevant headlines |
| 3 | Krebs on Security | `krebsonsecurity.com/feed/` | ☐ HTTP 200, valid XML | ☐ Author = Brian Krebs |
| 4 | BleepingComputer | `bleepingcomputer.com/feed/` | ☐ HTTP 200, valid XML | ☐ Breach/malware reporting |
| 5 | SecurityWeek | `feeds.feedburner.com/securityweek` | ☐ HTTP 200, valid XML | ☐ Enterprise security news |
| 6 | Schneier on Security | `schneier.com/blog/atom.xml` | ☐ HTTP 200, valid Atom | ☐ Crypto/privacy expert |
| 7 | CSO Online | `csoonline.com/feed/` | ☐ HTTP 200, valid XML | ☐ CISO-level reporting |
| 8 | Infosecurity Mag | `infosecurity-magazine.com/rss/news/` | ☐ HTTP 200, valid XML | ☐ UK-based InfoSec trade pub |
| 9 | Threatpost | `threatpost.com/feed` | ☐ HTTP 200, valid XML | ☐ Vulnerability/threat news |
| 10 | CyberScoop | `cyberscoop.com/feed/` | ☐ HTTP 200, valid XML | ☐ Gov/enterprise cyber news |
| 11 | The Record | `therecord.media/feed` | ☐ HTTP 200, valid XML | ☐ Investigative cyber journalism |
| 12 | Recorded Future | `recordedfuture.com/feed` | ☐ HTTP 200, valid XML | ☐ Threat intel content |
| 13 | SC Magazine | `scmagazine.com/home/feed/` | ☐ HTTP 200, valid XML | ☐ Cybersecurity trade pub |
| 14 | Hackread | `hackread.com/feed/` | ☐ HTTP 200, valid XML | ☐ Hacking/breach reporting |
| 15 | Security Affairs | `securityaffairs.com/feed` | ☐ HTTP 200, valid XML | ☐ European cyber perspective |
| 16 | Cisco Talos | `blog.talosintelligence.com/feeds/posts/default` | ☐ HTTP 200 | ☐ Threat intel research |
| 17 | Palo Alto Unit 42 | `unit42.paloaltonetworks.com/feed/` | ☐ HTTP 200 | ☐ APT/malware analysis |
| 18 | Google TAG | `blog.google/threat-analysis-group/rss/` | ☐ HTTP 200 | ☐ State-sponsored threat research |
| 19 | Microsoft Security | `microsoft.com/en-us/security/blog/feed/` | ☐ HTTP 200 | ☐ Enterprise security updates |
| 20 | CrowdStrike Blog | `crowdstrike.com/blog/feed/` | ☐ HTTP 200 | ☐ EDR/threat intel |
| 21 | SentinelOne Labs | `sentinelone.com/blog/feed/` | ☐ HTTP 200 | ☐ Endpoint research |
| 22 | Kaspersky Securelist | `securelist.com/feed/` | ☐ HTTP 200 | ☐ APT/malware deep dives |
| 23 | Sophos Naked Security | `nakedsecurity.sophos.com/feed/` | ☐ HTTP 200 | ☐ Consumer/enterprise security |
| 24 | ESET Research | `welivesecurity.com/feed/` | ☐ HTTP 200 | ☐ European threat research |
| 25 | Rapid7 Blog | `blog.rapid7.com/rss/` | ☐ HTTP 200 | ☐ Vulnerability research |
| 26 | Qualys Blog | `blog.qualys.com/feed` | ☐ HTTP 200 | ☐ Cloud security |
| 27 | CheckPoint Research | `research.checkpoint.com/feed/` | ☐ HTTP 200 | ☐ Threat intel |
| 28 | Fortinet Blog | `fortinet.com/blog/threat-research.xml` | ☐ HTTP 200 | ☐ FortiGuard research |
| 29 | Mandiant Blog | `cloud.google.com/blog/topics/threat-intelligence/rss/` | ☐ HTTP 200 | ☐ Incident response |
| 30 | Trend Micro Research | `trendmicro.com/en_us/research.html/rss.xml` | ☐ HTTP 200 | ☐ APT research |
| 31 | Proofpoint Blog | `proofpoint.com/us/blog.xml` | ☐ HTTP 200 | ☐ Email/phishing intel |
| 32 | Elastic Security Labs | `elastic.co/security-labs/rss/feed.xml` | ☐ HTTP 200 | ☐ Detection rules/research |
| 33 | Zero Day Initiative | `zerodayinitiative.com/rss/published/` | ☐ HTTP 200 | ☐ Vulnerability disclosures |
| 34 | Exploit-DB | `exploit-db.com/rss.xml` | ☐ HTTP 200 | ☐ Exploit PoCs |
| 35 | Packet Storm | `packetstormsecurity.com/files/feed/` | ☐ HTTP 200 | ☐ Security tools/exploits |
| 36 | CVE Details | `cvedetails.com/vulnerability-feed.php` | ☐ HTTP 200 | ☐ CVE vulnerability feed |
| 37 | VulnDB | `vuldb.com/?rss.recent` | ☐ HTTP 200 | ☐ Recent vulnerability entries |
| 38 | Troy Hunt (HIBP) | `troyhunt.com/rss/` | ☐ HTTP 200 | ☐ Breach expert blog |
| 39 | Malwarebytes Labs | `blog.malwarebytes.com/feed/` | ☐ HTTP 200 | ☐ Malware analysis |
| 40 | SANS Internet Storm | `isc.sans.edu/rssfeed_full.xml` | ☐ HTTP 200 | ☐ Threat diary entries |
| 41 | Abuse.ch | `abuse.ch/rss/` | ☐ HTTP 200 | ☐ Malware/botnet intel |
| 42 | DataBreaches.net | `databreaches.net/feed/` | ☐ HTTP 200 | ☐ Breach tracking |
| 43 | GrahamCluley | `grahamcluley.com/feed/` | ☐ HTTP 200 | ☐ Security commentary |
| 44 | AWS Security Blog | `aws.amazon.com/blogs/security/feed/` | ☐ HTTP 200 | ☐ Cloud security |
| 45 | Google Cloud Security | `cloud.google.com/blog/topics/security/rss/` | ☐ HTTP 200 | ☐ GCP security |
| 46 | Azure Security Blog | `azure.microsoft.com/en-us/blog/tag/security/feed/` | ☐ HTTP 200 | ☐ Azure security |
| 47 | Snyk Blog | `snyk.io/blog/feed/` | ☐ HTTP 200 | ☐ DevSecOps/SCA |
| 48 | CISA Alerts | `cisa.gov/cybersecurity-advisories/all.xml` | ☐ HTTP 200 | ☐ US gov advisories |
| 49 | NCSC UK | `ncsc.gov.uk/.../all-rss-feed.xml` | ☐ HTTP 200 | ☐ UK gov advisories |
| 50 | NCSC Nederland | `advisories.ncsc.nl/rss/advisories` | ☐ HTTP 200 | ☐ Dutch CERT |
| 51 | CERT-FR | `cert.ssi.gouv.fr/feed/` | ☐ HTTP 200 | ☐ French CERT |
| 52 | JPCERT | `jpcert.or.jp/english/rss/jpcert-en.rdf` | ☐ HTTP 200 | ☐ Japanese CERT |
| 53 | NSA Cybersecurity | `nsa.gov/Press-Room/.../rss/` | ☐ HTTP 200 | ☐ US NSA advisories |
| 54 | FBI Cyber | `fbi.gov/feeds/cyber-news/rss.xml` | ☐ HTTP 200 | ☐ FBI cyber alerts |
| 55 | Europol | `europol.europa.eu/rss` | ☐ HTTP 200 | ☐ EU law enforcement |
| 56 | CERT-IN India | `cert-in.org.in/RSS.xml` | ☐ HTTP 200 | ☐ Indian CERT |
| 57 | The Register Security | `theregister.com/security/headlines.atom` | ☐ HTTP 200 | ☐ UK tech/security |
| 58 | Heise Security | `heise.de/security/rss/news-atom.xml` | ☐ HTTP 200 | ☐ German security |
| 59 | Qihoo 360 Netlab | `blog.netlab.360.com/rss/` | ☐ HTTP 200 | ☐ Chinese threat research |
| 60 | KrCERT | `krcert.or.kr/rss.do` | ☐ HTTP 200 | ☐ Korean CERT |
| 61 | Cybersecurity News | `cybersecuritynews.com/feed/` | ☐ HTTP 200 | ☐ CVE/attack reporting |
| 62 | Reddit r/netsec | `reddit.com/r/netsec/.rss` | ☐ HTTP 200 | ☐ Security community |
| 63 | Reddit r/cybersecurity | `reddit.com/r/cybersecurity/.rss` | ☐ HTTP 200 | ☐ Cyber community |
| 64 | Hacker News | `hnrss.org/frontpage` | ☐ HTTP 200 | ☐ Tech community |
| 65 | Risky.Biz Newsletter | `risky.biz/feeds/risky-business/` | ☐ HTTP 200 | ☐ Security podcast/newsletter |
| 66 | SANS NewsBites | `sans.org/newsletters/newsbites/rss` | ☐ HTTP 200 | ☐ Curated security news |
| 67 | TechCrunch AI | `techcrunch.com/.../ai/feed/` | ☐ HTTP 200 | ☐ AI-specific articles |
| 68 | VentureBeat AI | `venturebeat.com/.../ai/feed/` | ☐ HTTP 200 | ☐ AI/ML industry |
| 69 | MIT Tech Review | `technologyreview.com/feed/` | ☐ HTTP 200 | ☐ Academic/research |
| 70 | Wired Security | `wired.com/.../security/.../rss` | ☐ HTTP 200 | ☐ Mainstream tech/security |
| 71 | BBC Technology | `feeds.bbci.co.uk/news/technology/rss.xml` | ☐ HTTP 200 | ☐ BBC branding, general tech |
| 72 | ZDNet Security | `zdnet.com/topic/security/rss.xml` | ☐ HTTP 200 | ☐ Enterprise security |
| 73 | The Verge Security | `theverge.com/rss/cyber-security/index.xml` | ☐ HTTP 200 | ☐ Consumer tech/security |
| 74 | Ars Technica Security | `feeds.arstechnica.com/arstechnica/security` | ☐ HTTP 200 | ☐ In-depth tech/security |
| 75 | NIST | `nist.gov/news-events/news/rss.xml` | ☐ HTTP 200 | ☐ Policy/standards |
| 76 | AI Now Institute | `ainowinstitute.org/feed` | ☐ HTTP 200 | ☐ AI policy/ethics |
| 77 | EFF Deeplinks | `eff.org/rss/updates.xml` | ☐ HTTP 200 | ☐ Digital rights/privacy |
| 78 | Lawfare | `lawfaremedia.org/feed` | ☐ HTTP 200 | ☐ National security law |
| 79 | Recorded Future Intel | `therecord.media/feed` | ☐ HTTP 200 | ☐ Threat intel reporting |

**Test procedure:**
```bash
# Automated: validate all 25 feeds in one pass
python3 -c "
import requests, feedparser
feeds = [
    ('The Hacker News',      'https://feeds.feedburner.com/TheHackersNews'),
    ('Dark Reading',         'https://www.darkreading.com/rss.xml'),
    ('Krebs on Security',    'https://krebsonsecurity.com/feed/'),
    ('CyberScoop',           'https://cyberscoop.com/feed/'),
    ('SANS ISC',             'https://isc.sans.edu/rssfeed_full.xml'),
    ('Recorded Future',      'https://www.recordedfuture.com/feed'),
    ('Cybersecurity News',   'https://cybersecuritynews.com/feed/'),
    ('The Record',           'https://therecord.media/feed'),
    ('Help Net Security',    'https://www.helpnetsecurity.com/feed/'),
    ('TechCrunch AI',        'https://techcrunch.com/category/artificial-intelligence/feed/'),
    ('VentureBeat AI',       'https://venturebeat.com/category/ai/feed/'),
    ('MIT Tech Review',      'https://www.technologyreview.com/feed/'),
    ('Hacker News YC',       'https://hnrss.org/frontpage'),
    ('NIST',                 'https://www.nist.gov/news-events/cybersecurity/rss.xml'),
    ('AI Now Institute',     'https://ainowinstitute.org/feed'),
    ('Security Affairs',     'https://securityaffairs.com/feed'),
    ('Infosecurity Mag',     'https://www.infosecurity-magazine.com/rss/news/'),
    ('NCSC UK',              'https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml'),
    ('NCSC NL',              'https://advisories.ncsc.nl/rss/advisories'),
    ('Wired Security',       'https://www.wired.com/feed/category/security/latest/rss'),
    ('BBC Tech',             'https://feeds.bbci.co.uk/news/technology/rss.xml'),
    ('ZDNet Security',       'https://www.zdnet.com/topic/security/rss.xml'),
    ('Hackread',             'https://www.hackread.com/feed/'),
    ('Threatpost',           'https://threatpost.com/feed'),
    ('JPCERT',               'https://www.jpcert.or.jp/english/rss/jpcert-en.rdf'),
]
for name, url in feeds:
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        f = feedparser.parse(r.content)
        n = len(f.entries)
        status = 'PASS' if r.status_code == 200 and n > 0 else 'FAIL'
        print(f'{status} | {name:25s} | HTTP {r.status_code} | {n} entries')
    except Exception as e:
        print(f'FAIL | {name:25s} | {e}')
"
```

**Pass criteria:** All 79 feeds return HTTP 200 with ≥1 entry containing `title` and `link`. Some feeds may intermittently 429 — the collector's exponential backoff handles this gracefully.

---

### 1.2 Certification Feeds (13 feeds)

| # | Body | URL | Auth Check | Content Check |
|---|---|---|---|---|
| 1 | NIST | `nist.gov/blogs/cybersecurity-insights/rss.xml` | ☐ .gov domain | ☐ Standards/framework content |
| 2 | SANS ISC | `isc.sans.edu/rssfeed_full.xml` | ☐ .edu domain | ☐ Threat diary entries |
| 3 | OWASP | `owasp.org/feed.xml` | ☐ OWASP Foundation | ☐ AppSec project updates |
| 4 | FIRST | `first.org/newsroom/releases/rss.xml` | ☐ FIRST.org (CVSS authority) | ☐ CSIRT coordination news |
| 5 | CISA | `cisa.gov/cybersecurity-advisories/all.xml` | ☐ .gov domain | ☐ US gov advisories |
| 6 | NCSC UK | `ncsc.gov.uk/.../all-rss-feed.xml` | ☐ .gov.uk domain | ☐ UK gov advisories |
| 7 | NCSC NL | `advisories.ncsc.nl/rss/advisories` | ☐ .nl gov domain | ☐ Dutch CERT advisories |
| 8 | ENISA | `enisa.europa.eu/publications/rss.xml` | ☐ .europa.eu | ☐ EU cybersecurity agency |
| 9 | CERT-FR | `cert.ssi.gouv.fr/feed/` | ☐ .gouv.fr | ☐ French CERT |
| 10 | JPCERT | `jpcert.or.jp/english/rss/jpcert-en.rdf` | ☐ .or.jp domain | ☐ Japanese CERT alerts |
| 11 | ACSC Australia | `cyber.gov.au/.../rss.xml` | ☐ .gov.au domain | ☐ Australian CERT |
| 12 | CERT-IN India | `cert-in.org.in/RSS.xml` | ☐ .org.in domain | ☐ Indian CERT |
| 13 | KrCERT Korea | `krcert.or.kr/rss.do` | ☐ .or.kr domain | ☐ Korean CERT |

**Test procedure:** Same as RSS — HTTP GET + feedparser validation.

**Pass criteria:** All 13 return valid entries. Each body's domain matches its claimed org.

---

### 1.3 NVD / CVE API

| Check | Expected |
|---|---|
| ☐ Endpoint `services.nvd.nist.gov/rest/json/cves/2.0` responds | HTTP 200 |
| ☐ Response contains `vulnerabilities[]` array | Valid JSON |
| ☐ Each CVE has `cve.id` matching `CVE-\d{4}-\d{4,}` | Regex match |
| ☐ CVSS scores present (v3.1 / v3.0 / v2) | ≥1 metric object per CVE |
| ☐ `pubStartDate/pubEndDate` filter works (48h window) | Results within range |
| ☐ `resultsPerPage=100` returns ≤100 results | Count check |
| ☐ Rate limiting: ≤5 req/30s without API key | No 403 errors |

**Test procedure:**
```bash
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5" | python3 -m json.tool | head -50
```

---

### 1.4 GDELT API

| Check | Expected |
|---|---|
| ☐ Endpoint `api.gdeltproject.org/api/v2/doc/doc` responds | HTTP 200 |
| ☐ `mode=artlist&format=json` returns JSON array | Valid JSON |
| ☐ Each article has `url`, `title`, `seendate`, `domain` | Required fields present |
| ☐ `tone` field is numeric (-100 to +100 range) | Float value |
| ☐ `sourcecountry` maps to known country codes | ISO codes |
| ☐ `timespan=72h` returns recent articles only | Within 72h window |
| ☐ All 21 queries return ≥1 result | Non-empty response |

**Test procedure:** Run each of the 21 GDELT queries and validate response:
```bash
python3 -c "
import httpx, json
queries = [
    'cybersecurity attack hacker', 'ransomware', 'data breach',
    'zero day vulnerability exploit', 'supply chain attack software',
    'critical infrastructure cyberattack', 'DDoS distributed denial service',
    'nation state hacking espionage', 'AI artificial intelligence policy',
    'AI ethics regulation', 'CISA cybersecurity United States',
    'Canada cyber attack', 'European cyber attack telecom',
    'NCSC Netherlands cyber', 'Japan cyber attack JPCERT',
    'Australia cyber attack ASD', 'India cyber attack CERT',
    'Singapore cyber security', 'South Korea cyber attack',
    'China cyber espionage APT',
]
for q in queries:
    r = httpx.get('https://api.gdeltproject.org/api/v2/doc/doc', params={
        'query': q, 'mode': 'artlist', 'maxrecords': 5,
        'timespan': '72h', 'sort': 'hybridrel', 'format': 'json'
    }, timeout=30)
    try:
        data = r.json()
        n = len(data.get('articles', []))
        print(f'{'PASS' if n > 0 else 'WARN'} | {q:45s} | {n} articles')
    except: print(f'FAIL | {q:45s} | Non-JSON response')
"
```

---

### 1.5 Yahoo Finance API

| Check | Expected |
|---|---|
| ☐ Endpoint `query1.finance.yahoo.com/v8/finance/chart/{ticker}` responds | HTTP 200 |
| ☐ Response has `chart.result[0].indicators.quote[0].close[]` | Price array |
| ☐ All 18 tickers return valid price data | Non-null close prices |
| ☐ `change_pct` calculation is correct (last vs previous close) | Math check |
| ☐ Ticker symbols match real NYSE/NASDAQ listings | Cross-reference |

**18 tickers to validate:**

| Ticker | Company | Sector | Listing Check |
|---|---|---|---|
| PANW | Palo Alto Networks | cybersecurity | ☐ NASDAQ |
| CRWD | CrowdStrike | cybersecurity | ☐ NASDAQ |
| FTNT | Fortinet | cybersecurity | ☐ NASDAQ |
| CHKP | Check Point | cybersecurity | ☐ NASDAQ |
| OKTA | Okta | cybersecurity | ☐ NASDAQ |
| RPD | Rapid7 | cybersecurity | ☐ NASDAQ |
| S | SentinelOne | cybersecurity | ☐ NYSE |
| CYBR | CyberArk | cybersecurity | ☐ NASDAQ |
| ZS | Zscaler | cybersecurity | ☐ NASDAQ |
| NVDA | NVIDIA | ai | ☐ NASDAQ |
| MSFT | Microsoft | ai | ☐ NASDAQ |
| GOOGL | Alphabet | ai | ☐ NASDAQ |
| META | Meta Platforms | ai | ☐ NASDAQ |
| AAPL | Apple | ai | ☐ NASDAQ |
| IBM | IBM | ai | ☐ NYSE |
| AMZN | Amazon | ai | ☐ NASDAQ |
| PLTR | Palantir | ai | ☐ NYSE |
| AI | C3.ai | ai | ☐ NYSE |

---

### 1.6 YouTube Data API

| Check | Expected |
|---|---|
| ☐ Requires `YOUTUBE_API_KEY` — returns `[]` if unset | Graceful skip |
| ☐ 6 search queries are cybersecurity/AI relevant | Topic alignment |
| ☐ `eventType=live` filter works | Only live streams |
| ☐ Deduplication by `video_id` | No duplicate entries |
| ☐ API key quota not exceeded (10,000 units/day) | Under limit |

---

## 2. Collector Accuracy

### 2.1 RSS Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ Parses `published_parsed` correctly | Feed sample w/ known date | `published_at` matches source |
| ☐ Falls back to `updated_parsed` | Feed without `published_parsed` | Date still populated |
| ☐ Title truncation at 512 chars | Synthetic long-title entry | `len(title) <= 512` |
| ☐ Summary truncation at 2048 chars | Synthetic entry | `len(summary) <= 2048` |
| ☐ URL truncation at 1024 chars | Synthetic entry | `len(source_url) <= 1024` |
| ☐ `external_id` = `sha256(link)[:64]` | Compute manually | Match |
| ☐ Max 20 entries per feed | Feed with 50+ entries | `len(results) <= 20 * num_feeds` |
| ☐ Per-feed error isolation | One feed 404, others fine | Other feeds still collected |
| ☐ Event types assigned correctly | Check output | NEWS/ALERT/POLICY per feed config |

**Test procedure:**
```python
# Unit test: run collector, validate output structure
import asyncio
from app.collectors.rss_collector import RSSCollector

async def test_rss():
    c = RSSCollector()
    results = await c.collect()
    assert len(results) > 0, "No results collected"
    for r in results[:5]:
        assert 'title' in r and len(r['title']) <= 512
        assert 'source_url' in r and r['source_url'].startswith('http')
        assert 'event_type' in r and r['event_type'] in ('NEWS','ALERT','POLICY')
        assert 'external_id' in r and len(r['external_id']) == 64
        assert 'source_name' in r
    print(f"PASS: {len(results)} events from RSS")

asyncio.run(test_rss())
```

---

### 2.2 CVE Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ `indicator_id` format | Regex | Matches `CVE-\d{4}-\d{4,}` |
| ☐ `title` format | String check | `"{CVE-ID}: {desc[:120]}"` |
| ☐ CVSS version fallback | CVE with only v2 | Score extracted |
| ☐ Severity mapping correct | CVSS 9.5 → CRITICAL | Enum match |
| ☐ Severity mapping correct | CVSS 7.2 → HIGH | Enum match |
| ☐ Severity mapping correct | CVSS 5.0 → MEDIUM | Enum match |
| ☐ Severity mapping correct | CVSS 2.1 → LOW | Enum match |
| ☐ Severity mapping correct | No CVSS → INFO | Enum match |
| ☐ `affected_products` max 20 | CVE with many CPEs | `len(products) <= 20` |
| ☐ `cwe_ids` max 10 | CVE with many CWEs | `len(cwe_ids) <= 10` |
| ☐ `references` max 10 | CVE with many refs | `len(refs) <= 10` |
| ☐ 48h time window | Check query params | `pubStartDate` = now - 48h |
| ☐ Timeout handling | Network delay | No crash, returns partial |

---

### 2.3 Financial Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ `price` is a valid float > 0 | All 18 tickers | Positive number |
| ☐ `change_pct` formula | Manual calc | `(last_close - prev_close) / prev_close * 100` |
| ☐ `volume` is integer | Type check | `isinstance(volume, int)` |
| ☐ `currency` defaults to USD | All tickers | `currency == "USD"` |
| ☐ Handles market-closed hours | Run on weekend | Returns last known data |
| ☐ 0.5s delay between tickers | Timing check | No rate-limit 429 errors |
| ☐ One ticker failure doesn't block others | Mock one 404 | 17 results returned |

---

### 2.4 GDELT Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ `sentiment_score` = `tone / 10.0` | Manual calc | Match to 4 decimals |
| ☐ `seendate` parsed as `%Y%m%dT%H%M%S` | Sample article | Valid datetime |
| ☐ Country→coordinate mapping | Country name lookup | Correct lat/lng |
| ☐ All 42 countries have valid coords | Iterate `COUNTRY_COORDS` | All tuples are `(float, float)` |
| ☐ Max 50 records per query | `maxrecords=50` | `len(articles) <= 50` |
| ☐ `extra` field stores `gdelt_tone` and `gdelt_domain` | Check output dict | Both keys present |
| ☐ Per-query error isolation | One query timeout | Others still collected |
| ☐ Deduplication across queries | Same article in 2 queries | Only 1 in output |

---

### 2.5 Cert Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ `standard_id` = `sha256(link)[:32]` | Manual calc | Match |
| ☐ `update_type` always `"announcement"` | Check output | Static value |
| ☐ `region` always `"Global"` | Check output | Static value |
| ☐ `body_name` matches feed config | Cross-reference | NIST/SANS/OWASP/FIRST/CISA/NCSC-UK/NCSC-NL/ENISA/CERT-FR/JPCERT/ACSC/CERT-IN/KrCERT |
| ☐ Max 10 entries per feed | Feed with 20+ entries | `len <= 10 * 13 = 130` |
| ☐ Per-feed error isolation | One feed 404 | Others still collected |

---

### 2.6 YouTube Collector

| Test | Method | Pass Criteria |
|---|---|---|
| ☐ Returns `[]` when `YOUTUBE_API_KEY` is empty | Unset key | Empty list |
| ☐ Deduplication by `video_id` | Same video in 2 queries | 1 result |
| ☐ `is_live` = `True` for live search | Check output | Boolean true |
| ☐ `category_tags` = first 4 words of query | String split | Match |
| ☐ `stream_url` format | URL check | `https://www.youtube.com/watch?v={id}` |
| ☐ 6 distinct search queries | Count | No duplicates |

---

## 3. Normalizer & Sentiment Pipeline

### 3.1 Sentiment Scoring (VADER)

| Test | Input | Expected Score | Range |
|---|---|---|---|
| ☐ Positive text | "Great security update released" | > 0.0 | 0.0 to 1.0 |
| ☐ Negative text | "Critical breach exposes millions" | < 0.0 | -1.0 to 0.0 |
| ☐ Neutral text | "NIST published framework update" | ≈ 0.0 | -0.2 to 0.2 |
| ☐ Empty string | "" | 0.0 | Exact |
| ☐ Round to 4 decimals | Any text | `len(str(score).split('.')[1]) <= 4` | Format |

**Test procedure:**
```python
from app.sentiment import score_sentiment
assert score_sentiment("") == 0.0
assert score_sentiment("Devastating ransomware attack") < 0.0
assert score_sentiment("Excellent security improvement") > 0.0
assert isinstance(score_sentiment("test"), float)
print("PASS: Sentiment scoring")
```

---

### 3.2 Impact Scoring

| Test | Keywords | Expected Score |
|---|---|---|
| ☐ High-impact single | "zero-day exploit discovered" | 5.0 (2 × 2.5) |
| ☐ High-impact stacked | "ransomware attack data breach malware" | 10.0 (capped) |
| ☐ Medium-impact | "patch update advisory" | 3.0 (3 × 1.0) |
| ☐ Mixed | "critical vulnerability patch released" | 6.0 (1×2.5 + 1×2.5 + 1×1.0) |
| ☐ No keywords | "Company announces new product line" | 0.0 |
| ☐ Cap at 10.0 | All 20 high-impact keywords | 10.0 |
| ☐ Case insensitive | "ZERO-DAY RANSOMWARE" | Same as lowercase |
| ☐ Tags contribute | title="test", text="", tags=["exploit"] | 2.5 |

**High-impact keywords to test (20):** `zero-day`, `ransomware`, `critical`, `nation-state`, `data breach`, `exploit`, `attack`, `vulnerability`, `breach`, `malware`, `apt`, `trojan`, `backdoor`, `infrastructure`, `emergency`, `leaked`, `compromised`, `stolen`, `hacked`

**Medium-impact keywords to test (15):** `patch`, `update`, `advisory`, `warning`, `threat`, `risk`, `exposure`, `disclosure`, `regulation`, `compliance`, `sanctions`, `ban`, `policy`, `fine`, `lawsuit`

---

### 3.3 Upsert Logic

| Test | Function | Check | Pass Criteria |
|---|---|---|---|
| ☐ New event insert | `upsert_events()` | DB row created | Row exists with all fields |
| ☐ Duplicate URL update | `upsert_events()` | `title`, `summary`, `sentiment_score`, `impact_score`, `updated_at` updated | Old row updated, not duplicated |
| ☐ Threat upsert on `indicator_id` | `upsert_threats()` | Duplicate CVE ID | Row updated, count unchanged |
| ☐ Financial always inserts | `insert_financial()` | Same ticker twice | 2 rows (time-series) |
| ☐ Stream upsert on `video_id` | `upsert_streams()` | Duplicate video | `is_live`, `viewer_count` updated |
| ☐ Cert always inserts | `upsert_certifications()` | Same cert twice | 2 rows |
| ☐ `_clean()` filters bad columns | Dict with `{'bad_col': 1}` | Key removed |
| ☐ Auto sentiment enrichment | Event without score | `sentiment_score` populated after upsert |
| ☐ Auto impact enrichment | Event without score | `impact_score` populated after upsert |

---

## 4. Database Integrity

### 4.1 Schema Validation

| Table | Check | SQL Query |
|---|---|---|
| ☐ `intelligence_events` exists | `\d intelligence_events` | 24 columns |
| ☐ `source_url` unique constraint | Insert duplicate | `IntegrityError` or upsert |
| ☐ `event_type` NOT NULL | Insert without type | Rejected |
| ☐ `financial_snapshots` exists | `\d financial_snapshots` | 16 columns |
| ☐ `live_streams` exists | `\d live_streams` | 14 columns |
| ☐ `video_id` unique constraint | Insert duplicate | `IntegrityError` or upsert |
| ☐ `threat_indicators` exists | `\d threat_indicators` | 18 columns |
| ☐ `indicator_id` unique constraint | Insert duplicate | `IntegrityError` or upsert |
| ☐ `certification_updates` exists | `\d certification_updates` | 12 columns |

### 4.2 Index Performance

| Index | Table | Column(s) | Verify |
|---|---|---|---|
| ☐ `ix_intel_event_type` | `intelligence_events` | `event_type` | `\di ix_intel_event_type` |
| ☐ `ix_intel_published_at` | `intelligence_events` | `published_at` | Exists |
| ☐ `ix_intel_impact_score` | `intelligence_events` | `impact_score` | Exists |
| ☐ `ix_intel_country` | `intelligence_events` | `country` | Exists |
| ☐ `ix_fin_ticker` | `financial_snapshots` | `ticker` | Exists |
| ☐ `ix_fin_snapshot_at` | `financial_snapshots` | `snapshot_at` | Exists |
| ☐ `ix_threat_severity` | `threat_indicators` | `severity` | Exists |
| ☐ `ix_threat_cvss` | `threat_indicators` | `cvss_score` | Exists |

### 4.3 Data Quality Queries

```sql
-- Events with NULL required fields
SELECT COUNT(*) FROM intelligence_events WHERE title IS NULL OR source_url IS NULL OR event_type IS NULL;
-- Expected: 0

-- Sentiment score out of range
SELECT COUNT(*) FROM intelligence_events WHERE sentiment_score < -1.0 OR sentiment_score > 1.0;
-- Expected: 0

-- Impact score out of range
SELECT COUNT(*) FROM intelligence_events WHERE impact_score < 0.0 OR impact_score > 10.0;
-- Expected: 0

-- CVSS out of range
SELECT COUNT(*) FROM threat_indicators WHERE cvss_score < 0.0 OR cvss_score > 10.0;
-- Expected: 0

-- Financial price negative
SELECT COUNT(*) FROM financial_snapshots WHERE price < 0;
-- Expected: 0

-- Duplicate source_urls (should be 0 due to UNIQUE constraint)
SELECT source_url, COUNT(*) FROM intelligence_events GROUP BY source_url HAVING COUNT(*) > 1;
-- Expected: 0 rows

-- Duplicate indicator_ids
SELECT indicator_id, COUNT(*) FROM threat_indicators GROUP BY indicator_id HAVING COUNT(*) > 1;
-- Expected: 0 rows

-- Event type distribution (diversity check)
SELECT event_type, COUNT(*) FROM intelligence_events GROUP BY event_type ORDER BY COUNT(*) DESC;
-- Expected: NEWS, ALERT, POLICY all represented

-- Source name distribution
SELECT source_name, COUNT(*) FROM intelligence_events GROUP BY source_name ORDER BY COUNT(*) DESC;
-- Expected: ≥15 distinct sources with data
```

---

## 5. API Endpoint Accuracy

### 5.1 Intelligence Router (`/api/v1/intelligence`)

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ List events | `GET /` | 200, `PaginatedResponse` with `items[]` |
| 2 | ☐ Pagination | `GET /?page=2&page_size=5` | `page=2`, `items.length <= 5` |
| 3 | ☐ Filter by event_type | `GET /?event_type=NEWS` | All items have `event_type=NEWS` |
| 4 | ☐ Filter by country | `GET /?country=United States` | All items have matching country |
| 5 | ☐ Filter by source_name | `GET /?source_name=NIST` | All items from NIST |
| 6 | ☐ Search keyword | `GET /?search=ransomware` | Title/summary contains keyword |
| 7 | ☐ Min impact filter | `GET /?min_impact=7` | All items have `impact_score >= 7` |
| 8 | ☐ Top by impact | `GET /top?n=5` | 5 items, sorted by `impact_score` desc |
| 9 | ☐ Map events | `GET /map` | All items have non-null `latitude`, `longitude` |
| 10 | ☐ Map filter | `GET /map?event_type=ALERT` | All items are ALERT type with coords |
| 11 | ☐ Stats | `GET /stats` | `{total: int, by_type: {}, top_countries: []}` |
| 12 | ☐ Invalid event_type | `GET /?event_type=INVALID` | 200, empty result set (0 items) |
| 13 | ☐ page_size > 100 | `GET /?page_size=200` | 422 validation error |
| 14 | ☐ page < 1 | `GET /?page=0` | 422 validation error |

**Test procedure:**
```bash
BASE="http://localhost:8443/api/v1"

# Basic list
curl -s "$BASE/intelligence/" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Total: {d[\"total\"]}, Items: {len(d[\"items\"])}')"

# Top events
curl -s "$BASE/intelligence/top?n=5" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Top 5: {[e[\"impact_score\"] for e in d]}')"

# Map
curl -s "$BASE/intelligence/map" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Map events: {len(d)}, all geotagged: {all(e[\"latitude\"] for e in d)}')"

# Stats
curl -s "$BASE/intelligence/stats" | python3 -m json.tool
```

---

### 5.2 Threats Router (`/api/v1/threats`)

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ List threats | `GET /` | 200, paginated response |
| 2 | ☐ Filter severity | `GET /?severity=CRITICAL` | All items `severity=CRITICAL` |
| 3 | ☐ Filter min CVSS | `GET /?min_cvss=9.0` | All items `cvss_score >= 9.0` |
| 4 | ☐ Search CVE | `GET /?search=CVE-2024` | Title contains search term |
| 5 | ☐ Critical endpoint | `GET /critical?limit=10` | ≤10 items, severity IN (CRITICAL, HIGH) |
| 6 | ☐ CVSS ordering | `GET /critical` | Sorted by `cvss_score` descending |

---

### 5.3 Financial Router (`/api/v1/financial`)

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ Latest snapshots | `GET /` | 1 row per ticker (18 max) |
| 2 | ☐ Sector filter | `GET /?sector=cybersecurity` | Only cyber tickers (9) |
| 3 | ☐ Sector filter | `GET /?sector=ai` | Only AI tickers (9) |
| 4 | ☐ Ticker history | `GET /PANW/history?limit=10` | ≤10 rows for PANW, chronological |
| 5 | ☐ Movers | `GET /movers` | `{gainers: [≤5], losers: [≤5]}` |
| 6 | ☐ Invalid ticker | `GET /ZZZZZ/history` | 200, empty list |
| 7 | ☐ Ticker case insensitive | `GET /panw/history` | Same as PANW (uppercased) |

---

### 5.4 Streams Router (`/api/v1/streams`)

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ All streams | `GET /` | 200, list of streams |
| 2 | ☐ Live only filter | `GET /?live_only=true` | All items have `is_live=true` |
| 3 | ☐ Sort order | `GET /` | Sorted by `is_live desc`, `viewer_count desc` |

---

### 5.5 Certifications Router (`/api/v1/certifications`)

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ List certs | `GET /` | 200, paginated response |
| 2 | ☐ Filter body | `GET /?body_name=NIST` | All items `body_name` contains "NIST" |
| 3 | ☐ Filter region | `GET /?region=Global` | All items `region` contains "Global" |
| 4 | ☐ Bodies list | `GET /bodies` | ≥13 body names returned |
| 5 | ☐ Pagination | `GET /?page=1&page_size=10` | ≤10 items, total/pages correct |

---

### 5.6 Health & CORS

| # | Test | Request | Pass Criteria |
|---|---|---|---|
| 1 | ☐ Health check | `GET /health` | `{"status": "ok", "version": "1.0.0"}` |
| 2 | ☐ CORS headers | `OPTIONS /api/v1/intelligence/` | `Access-Control-Allow-Origin` present |
| 3 | ☐ Allowed origin | Origin: `http://localhost:1337` | Allowed |
| 4 | ☐ Blocked origin | Origin: `http://evil.com` | No CORS header |
| 5 | ☐ Docs endpoint | `GET /docs` | Swagger UI HTML |
| 6 | ☐ ReDoc endpoint | `GET /redoc` | ReDoc HTML |

---

## 6. Frontend Rendering & UX

### 6.1 Dashboard View (`/`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ 4 KPI cards render | Total Events, Threat Alerts, Tracked Stocks, Live Streams visible |
| 2 | ☐ KPI values are non-zero after collection | Numbers > 0 |
| 3 | ☐ Values > 9999 display as "Xk" | StatCard formatting |
| 4 | ☐ Top 6 impact events render | EventCards with impact badges |
| 5 | ☐ Critical CVEs section | ≤5 CVEs with severity badges |
| 6 | ☐ Market movers section | 3 gainers (green) + 2 losers (red) |
| 7 | ☐ All data loads via `Promise.all` | No sequential waterfall in Network tab |

---

### 6.2 Intelligence View (`/intelligence`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Event type dropdown | 8 options: NEWS, POLICY, PRODUCT, FINANCIAL, VIDEO, CERTIFICATION, STARTUP, ALERT |
| 2 | ☐ Search input works | Type "ransomware", press Enter → filtered results |
| 3 | ☐ Min impact slider | Set to 5 → only impact ≥ 5 shown |
| 4 | ☐ Pagination controls | Next/Prev buttons, page number display |
| 5 | ☐ EventCard links open source URL | Click → new tab with original article |
| 6 | ☐ Category tags display | Max 4 tags per card |
| 7 | ☐ Impact badge colors | ≥7 red, ≥4 yellow, <4 gray |
| 8 | ☐ URL query param | Navigate to `/intelligence?search=test` → auto-searches |

---

### 6.3 Threat Intel View (`/threats`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Table columns | CVE ID, Severity, CVSS, Title, Published |
| 2 | ☐ Severity badges | CRITICAL=red, HIGH=orange, MEDIUM=yellow, LOW=blue, INFO=gray |
| 3 | ☐ CVSS color coding | Score displayed with appropriate color |
| 4 | ☐ Severity filter dropdown | CRITICAL/HIGH/MEDIUM/LOW/INFO |
| 5 | ☐ Search by CVE ID | "CVE-2024" → matching results |
| 6 | ☐ Pagination | Pages navigate correctly |
| 7 | ☐ Date format | `MM/dd HH:mm` (via date-fns) |

---

### 6.4 World Map View (`/map`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Leaflet map renders | Dark CartoDB tiles visible |
| 2 | ☐ Circle markers appear | ≥1 marker on map |
| 3 | ☐ Marker radius scales with impact | Higher impact = larger circle (6 + score) |
| 4 | ☐ Marker colors | ≥8 red, ≥5 gold, ≥3 cyan, <3 green |
| 5 | ☐ Popup on click | Shows title, source, country |
| 6 | ☐ Event type filter | Dropdown filters markers |
| 7 | ☐ Event count displayed | "X geotagged events" text |
| 8 | ☐ Geographic spread | Markers on ≥3 continents (NAM, EMEA, APAC) |

---

### 6.5 Financial View (`/financial`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Stock grid cards | 18 cards (or filtered subset) |
| 2 | ☐ Price display | Positive number with $ |
| 3 | ☐ Change % color | Positive = green, Negative = red |
| 4 | ☐ Sector filter buttons | "All", "cybersecurity", "ai" |
| 5 | ☐ Click card → TrendChart | Price history chart appears |
| 6 | ☐ Chart renders with data | Line chart with ≥2 data points |
| 7 | ☐ Date format on chart | `MM/dd HH:mm` |

---

### 6.6 Live Streams View (`/streams`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Stream cards render | Thumbnail, title, channel |
| 2 | ☐ LIVE badge pulsing | Red pulsing dot on live streams |
| 3 | ☐ Viewer count displayed | Number formatted |
| 4 | ☐ "Live only" toggle | Checkbox filters to `is_live=true` |
| 5 | ☐ YouTube link works | Card links to `youtube.com/watch?v=...` |
| 6 | ☐ Category tags shown | Tag pills on cards |

---

### 6.7 Certifications View (`/certifications`)

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ Body name pill filters | Clickable pills for each body |
| 2 | ☐ Cards display | Title, body badge, region, update type, date |
| 3 | ☐ Title links to source | Anchor opens original URL |
| 4 | ☐ Region/type info shown | "Global", "announcement" or actual values |
| 5 | ☐ Pagination | page_size=50, navigation works |
| 6 | ☐ Bodies endpoint returns list | ≥13 standardization bodies |

---

### 6.8 Layout Components

| # | Component | Test | Pass Criteria |
|---|---|---|---|
| 1 | ☐ AppSidebar | 7 navigation links | All routes work |
| 2 | ☐ AppSidebar | Active route highlight | Accent border on current page |
| 3 | ☐ AppSidebar | CyberVerse logo | Pulsing green dot animation |
| 4 | ☐ AppNavbar | Search bar | Enter navigates to `/intelligence?search=...` |
| 5 | ☐ AppNavbar | Refresh button | Page reload triggered |
| 6 | ☐ AppNavbar | UTC clock | Updates every second, shows UTC time |
| 7 | ☐ AppNavbar | LIVE indicator | Pulsing red dot |
| 8 | ☐ AppFooter | Static text | "CyberVerse Intelligence Aggregator" visible |
| 9 | ☐ Router | Catch-all redirect | `/nonexistent` → `/` |
| 10 | ☐ Router | Page transitions | Fade animation between views |

---

## 7. Infrastructure & Deployment

### 7.1 Docker Compose

| # | Test | Command | Pass Criteria |
|---|---|---|---|
| 1 | ☐ Full build | `docker compose up --build` | All 3 services start |
| 2 | ☐ Postgres healthy | `docker compose exec postgres pg_isready` | "accepting connections" |
| 3 | ☐ Backend reachable | `curl http://localhost:8443/health` | `{"status": "ok"}` |
| 4 | ☐ Frontend reachable | `curl http://localhost:1337` | HTML response |
| 5 | ☐ API proxy works | `curl http://localhost:1337/api/v1/intelligence/stats` | JSON response (not 502) |
| 6 | ☐ Postgres volume persists | `docker compose down && docker compose up` | Data retained |
| 7 | ☐ pgAdmin accessible | `docker compose --profile dev up pgadmin` | http://localhost:5050 loads |
| 8 | ☐ Alembic migration | Backend container log: `alembic upgrade head` | Tables created |
| 9 | ☐ Scheduler starts | Backend log: "ready" | Collection jobs registered |
| 10 | ☐ Backend hot reload | Edit Python file | Uvicorn auto-reloads (dev mount) |

### 7.2 Nginx Configuration

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ `/api/*` proxied to backend | Response from FastAPI |
| 2 | ☐ SPA fallback | `/intelligence` returns `index.html` |
| 3 | ☐ Gzip enabled | `Content-Encoding: gzip` for JS/CSS |
| 4 | ☐ Static asset caching | `Cache-Control: public, max-age=2592000` for `.js`/`.css` |
| 5 | ☐ X-Forwarded-For header | Backend receives real client IP |
| 6 | ☐ Proxy timeout 60s | Long API calls don't 504 |

### 7.3 Security

| # | Test | Pass Criteria |
|---|---|---|
| 1 | ☐ No SQL injection | `?search=' OR 1=1--` | Parameterized query, no data leak |
| 2 | ☐ No XSS in API | `?search=<script>alert(1)</script>` | Escaped in response |
| 3 | ☐ CORS blocks unknown origins | `Origin: http://evil.com` | No `Access-Control-Allow-Origin` |
| 4 | ☐ No sensitive data in logs | Check container logs | No passwords, API keys |
| 5 | ☐ Database credentials not in code | Grep for passwords | Only in `.env` / docker-compose |
| 6 | ☐ Input length limits | 10KB search string | No memory exhaustion |
| 7 | ☐ Rate limiting on NVD API | Multiple rapid CVE calls | Graceful backoff |

---

## 8. Diversity & Coverage Audit

### 8.1 Geographic Diversity

| Region | RSS Sources | GDELT Queries | Cert Bodies | Pass Criteria |
|---|---|---|---|---|
| ☐ **NAM (North America)** | The Hacker News, Dark Reading, Krebs, CyberScoop, SANS, Recorded Future, The Record, TechCrunch, VentureBeat, MIT Tech, HN, NIST, AI Now, SC Magazine, DataBreaches.net, AWS Security Blog | CISA USA, Canada | NIST, CISA, SANS | ≥15 NAM sources |
| ☐ **EMEA (Europe/ME/Africa)** | Security Affairs (IT), Infosecurity Mag (UK), NCSC UK, NCSC NL, CERT-FR, Heise Security (DE), The Register (UK), Europol, ENISA, EFF, Lawfare | European telecom, NCSC Netherlands | NCSC-UK, NCSC-NL, ENISA, CERT-FR, OWASP, FIRST | ≥8 EMEA sources |
| ☐ **APAC (Asia-Pacific)** | JPCERT (JP), CERT-IN (IN), KrCERT (KR), ACSC (AU), Qihoo 360 Netlab (CN) | Japan, Australia, India, Singapore, South Korea, China | JPCERT, ACSC, CERT-IN, KrCERT | ≥5 RSS + ≥6 GDELT queries |
| ☐ **Global** | Wired, BBC, ZDNet, Hackread, Threatpost, Ars Technica, The Verge, Reddit, Risky.Biz, SANS NewsBites, GrahamCluley, Snyk | Cybersecurity, ransomware, data breach, zero-day, supply chain, DDoS, nation-state | OWASP, FIRST | ≥10 global sources |

**Validation query:**
```sql
-- Geographic distribution of events
SELECT country, COUNT(*) as event_count
FROM intelligence_events
WHERE country IS NOT NULL
GROUP BY country
ORDER BY event_count DESC;
-- Expected: ≥5 distinct countries with ≥10 events each

-- Source name diversity
SELECT source_name, COUNT(*) as event_count
FROM intelligence_events
GROUP BY source_name
ORDER BY event_count DESC;
-- Expected: ≥15 distinct sources active
```

---

### 8.2 Topical Diversity

| Topic Area | Sources Covering | Verification |
|---|---|---|
| ☐ **Cybersecurity attacks** | THN, Dark Reading, Krebs, CyberScoop, Security Affairs, Hackread, GDELT (7 queries) | `event_type=NEWS` with attack keywords |
| ☐ **Vulnerabilities/CVE** | NVD API (CVE collector), SANS ISC | `threat_indicators` table has data |
| ☐ **AI/ML** | TechCrunch AI, VentureBeat AI, MIT Tech Review, GDELT (2 AI queries) | Search "AI" returns results |
| ☐ **Policy/Regulation** | NIST, AI Now Institute, GDELT AI policy | `event_type=POLICY` has entries |
| ☐ **Government advisories** | NCSC UK, NCSC NL, JPCERT, CISA (GDELT) | `event_type=ALERT` has entries |
| ☐ **Financial markets** | 18 tickers (9 cyber + 9 AI) | `financial_snapshots` has all 18 |
| ☐ **Live streams** | YouTube (6 queries) | `live_streams` has entries (if API key set) |
| ☐ **Standards/Certs** | NIST, OWASP, FIRST, CISA, NCSC-UK, NCSC-NL, ENISA, CERT-FR, JPCERT, ACSC, CERT-IN, KrCERT, SANS | `certification_updates` has data |

**Validation query:**
```sql
-- Event type distribution
SELECT event_type, COUNT(*) FROM intelligence_events GROUP BY event_type;
-- Expected: at least NEWS, ALERT, POLICY all > 0

-- Cert body distribution
SELECT body_name, COUNT(*) FROM certification_updates GROUP BY body_name;
-- Expected: ≥5 distinct bodies with data

-- Financial sector distribution
SELECT sector, COUNT(DISTINCT ticker) FROM financial_snapshots GROUP BY sector;
-- Expected: cybersecurity=9, ai=9
```

---

### 8.3 Sector Diversity (Financial)

| Sector | # Tickers | Companies | Check |
|---|---|---|---|
| ☐ Cybersecurity | 9 | PANW, CRWD, FTNT, CHKP, OKTA, RPD, S, CYBR, ZS | All have price data |
| ☐ AI/Tech | 9 | NVDA, MSFT, GOOGL, META, AAPL, IBM, AMZN, PLTR, AI | All have price data |

---

### 8.4 Temporal Diversity

| Check | Query | Pass Criteria |
|---|---|---|
| ☐ Recent data | `SELECT MAX(published_at) FROM intelligence_events` | Within 24h of now |
| ☐ Continuous collection | `SELECT date_trunc('hour', collected_at), COUNT(*) FROM intelligence_events GROUP BY 1 ORDER BY 1 DESC LIMIT 24` | Events in multiple hours |
| ☐ CVE freshness | `SELECT MAX(published_at) FROM threat_indicators` | Within 48h |
| ☐ Financial freshness | `SELECT MAX(snapshot_at) FROM financial_snapshots` | Within market hours |

---

## 9. End-to-End Scenarios

### 9.1 Full Data Pipeline

```
Scenario: A new CVE is published on NVD
1. ☐ CVE collector fetches it within 30 minutes
2. ☐ Row inserted in `threat_indicators` with correct severity/CVSS
3. ☐ GET /api/v1/threats/ returns the new CVE
4. ☐ GET /api/v1/threats/critical includes it (if CRITICAL/HIGH)
5. ☐ Dashboard shows updated threat count
6. ☐ ThreatIntelView table shows the new row
```

### 9.2 RSS → Intelligence Event Pipeline

```
Scenario: A breaking cybersecurity news article is published
1. ☐ RSS collector picks it up within 15 minutes
2. ☐ Sentiment score assigned (-1.0 to +1.0)
3. ☐ Impact score assigned (0–10) based on keyword heuristics
4. ☐ Row upserted in `intelligence_events`
5. ☐ GET /api/v1/intelligence/ returns the event
6. ☐ If high-impact, appears in /top endpoint
7. ☐ IntelligenceView shows the event card
8. ☐ Dashboard KPI "Total Events" increments
```

### 9.3 GDELT → World Map Pipeline

```
Scenario: A cyberattack in Japan is reported globally
1. ☐ GDELT "Japan cyber attack JPCERT" query finds the article
2. ☐ Country "Japan" mapped to coordinates (36.20, 138.25)
3. ☐ Sentiment derived from GDELT tone
4. ☐ Event upserted with latitude/longitude
5. ☐ GET /api/v1/intelligence/map returns the event
6. ☐ WorldMap shows a marker in Japan
7. ☐ Marker popup shows title and "Japan"
```

### 9.4 Financial Snapshot Pipeline

```
Scenario: Market closes with CrowdStrike up 5%
1. ☐ Financial collector runs (60-min interval)
2. ☐ CRWD snapshot inserted with correct price, change_pct
3. ☐ GET /api/v1/financial/ shows latest CRWD data
4. ☐ GET /api/v1/financial/movers includes CRWD in gainers
5. ☐ GET /api/v1/financial/CRWD/history shows time-series
6. ☐ FinancialView card shows green +5%
7. ☐ Dashboard "Market Movers" shows CRWD
```

### 9.5 Scheduler Resilience

```
Scenario: One collector fails, others continue
1. ☐ Simulate RSS feed timeout (all feeds unreachable)
2. ☐ GDELT and Cert collectors still run successfully
3. ☐ CVE collector (separate job) unaffected
4. ☐ Financial collector (separate job) unaffected
5. ☐ No crash, no scheduler stoppage
6. ☐ Error logged but not propagated
7. ☐ Next cycle: RSS collector retries and recovers
```

### 9.6 Upsert Idempotency

```
Scenario: Same article collected twice (RSS + GDELT overlap)
1. ☐ First insert creates row with source_url
2. ☐ Second attempt hits UNIQUE constraint on source_url
3. ☐ Upsert updates title, summary, scores, updated_at
4. ☐ No duplicate row created
5. ☐ COUNT stays the same
```

---

## Test Execution Checklist

| Phase | Tests | Status |
|---|---|---|
| **Phase 1: Source Liveness** | §1.1–§1.6 (all URLs reachable) | ☐ |
| **Phase 2: Collector Unit Tests** | §2.1–§2.6 (output structure/accuracy) | ☐ |
| **Phase 3: Sentiment & Normalizer** | §3.1–§3.3 (scoring, upsert logic) | ☐ |
| **Phase 4: Database Integrity** | §4.1–§4.3 (schema, indexes, data quality) | ☐ |
| **Phase 5: API Endpoints** | §5.1–§5.6 (all routes, filters, edge cases) | ☐ |
| **Phase 6: Frontend UI** | §6.1–§6.8 (rendering, interaction, navigation) | ☐ |
| **Phase 7: Infrastructure** | §7.1–§7.3 (Docker, Nginx, security) | ☐ |
| **Phase 8: Diversity Audit** | §8.1–§8.4 (geo, topic, sector, temporal) | ☐ |
| **Phase 9: End-to-End** | §9.1–§9.6 (full pipeline scenarios) | ☐ |
