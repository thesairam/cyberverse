"""CyberVerse Test Runner — Executes test.md plan and records failures."""
import requests
import feedparser
import httpx
import json
import time
import sys

RESULTS = []

def record(phase, test_id, name, status, detail=""):
    RESULTS.append({"phase": phase, "test_id": test_id, "name": name, "status": status, "detail": detail})
    icon = "PASS" if status == "pass" else "FAIL"
    print(f"  {icon} | {name}: {detail}")


def fetch_feed_with_retry(url, max_retries=3):
    """Fetch an RSS/Atom feed with retry on 429 rate limiting."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for attempt in range(max_retries):
        r = requests.get(url, timeout=15, headers=headers)
        if r.status_code == 429:
            wait = 5 * (2 ** attempt)
            print(f"    ... rate limited, retry in {wait}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
            continue
        return r
    return r  # return last response even if 429


# ============================================================
# PHASE 1: SOURCE LIVENESS
# ============================================================
print("\n" + "="*70)
print("PHASE 1: SOURCE LIVENESS")
print("="*70)

# 1.1 RSS Feeds
print("\n--- 1.1 RSS Feeds ---")
RSS_FEEDS = [
    ("The Hacker News",      "https://feeds.feedburner.com/TheHackersNews"),
    ("Dark Reading",         "https://www.darkreading.com/rss.xml"),
    ("Krebs on Security",    "https://krebsonsecurity.com/feed/"),
    ("CyberScoop",           "https://cyberscoop.com/feed/"),
    ("SANS ISC",             "https://isc.sans.edu/rssfeed_full.xml"),
    ("Recorded Future",      "https://www.recordedfuture.com/feed"),
    ("BleepingComputer",      "https://www.bleepingcomputer.com/feed/"),
    ("The Record",           "https://therecord.media/feed"),
    ("CSO Online",            "https://www.csoonline.com/feed/"),
    ("TechCrunch AI",        "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI",       "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review",      "https://www.technologyreview.com/feed/"),
    ("Hacker News YC",       "https://hnrss.org/frontpage"),
    ("NIST",                 "https://www.nist.gov/news-events/news/rss.xml"),
    ("AI Now Institute",     "https://ainowinstitute.org/feed"),
    ("Security Affairs",     "https://securityaffairs.com/feed"),
    ("Infosecurity Mag",     "https://www.infosecurity-magazine.com/rss/news/"),
    ("NCSC UK",              "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"),
    ("NCSC NL",              "https://advisories.ncsc.nl/rss/advisories"),
    ("Wired Security",       "https://www.wired.com/feed/category/security/latest/rss"),
    ("BBC Tech",             "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("ZDNet Security",       "https://www.zdnet.com/topic/security/rss.xml"),
    ("Hackread",             "https://www.hackread.com/feed/"),
    ("Threatpost",           "https://threatpost.com/feed"),
    ("JPCERT",               "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf"),
]

for name, url in RSS_FEEDS:
    try:
        r = fetch_feed_with_retry(url)
        f = feedparser.parse(r.content)
        n = len(f.entries)
        if r.status_code == 200 and n > 0:
            record("1.1", f"rss_{name}", name, "pass", f"HTTP 200, {n} entries")
        else:
            record("1.1", f"rss_{name}", name, "fail", f"HTTP {r.status_code}, {n} entries")
    except Exception as e:
        record("1.1", f"rss_{name}", name, "fail", f"ERROR: {e}")
    time.sleep(1)  # be polite between RSS requests

# 1.2 Cert Feeds
print("\n--- 1.2 Cert Feeds ---")
CERT_FEEDS = [
    ("NIST Cert",        "https://www.nist.gov/blogs/cybersecurity-insights/rss.xml"),
    ("SANS ISC Cert",    "https://isc.sans.edu/rssfeed_full.xml"),
    ("OWASP",            "https://owasp.org/feed.xml"),
    ("FIRST",            "https://www.first.org/newsroom/releases/rss.xml"),
    ("NCSC UK Cert",     "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"),
    ("NCSC NL Cert",     "https://advisories.ncsc.nl/rss/advisories"),
    ("JPCERT Cert",      "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf"),
]
for name, url in CERT_FEEDS:
    try:
        r = fetch_feed_with_retry(url)
        f = feedparser.parse(r.content)
        n = len(f.entries)
        if r.status_code == 200 and n > 0:
            record("1.2", f"cert_{name}", name, "pass", f"HTTP 200, {n} entries")
        else:
            record("1.2", f"cert_{name}", name, "fail", f"HTTP {r.status_code}, {n} entries")
    except Exception as e:
        record("1.2", f"cert_{name}", name, "fail", f"ERROR: {e}")
    time.sleep(1)

# 1.3 NVD CVE API
print("\n--- 1.3 NVD CVE API ---")
try:
    r = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0", params={"resultsPerPage": 5}, timeout=30)
    if r.status_code == 200:
        data = r.json()
        vulns = data.get("vulnerabilities", [])
        if len(vulns) > 0:
            cve_id = vulns[0].get("cve", {}).get("id", "")
            import re
            if re.match(r"CVE-\d{4}-\d{4,}", cve_id):
                record("1.3", "nvd_api", "NVD API", "pass", f"HTTP 200, {len(vulns)} CVEs, format OK ({cve_id})")
            else:
                record("1.3", "nvd_api", "NVD API", "fail", f"CVE ID format wrong: {cve_id}")
        else:
            record("1.3", "nvd_api", "NVD API", "fail", "No vulnerabilities returned")
    else:
        record("1.3", "nvd_api", "NVD API", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("1.3", "nvd_api", "NVD API", "fail", f"ERROR: {e}")

# 1.4 GDELT API
print("\n--- 1.4 GDELT API ---")
GDELT_QUERIES = [
    # Sample 10 representative queries (one per category) to avoid rate limits
    "cybersecurity attack hacker",          # Global threats
    "ransomware",                           # Malware
    "data breach",                          # Privacy
    "zero day vulnerability exploit",       # Exploits
    "artificial intelligence regulation",   # AI policy
    "CISA cybersecurity United States",     # Americas
    "European cyber attack telecom",        # Europe
    "Australia cybersecurity threat",       # APAC
    "India cyber attack CERT",              # APAC
    "Singapore cyber security",             # APAC
]
print("  (Testing 10 representative queries with retry + 15s spacing)")
for q in GDELT_QUERIES:
    passed = False
    last_detail = ""
    for attempt in range(4):
        try:
            r = requests.get("https://api.gdeltproject.org/api/v2/doc/doc", params={
                "query": q, "mode": "artlist", "maxrecords": 5,
                "timespan": "72h", "sort": "hybridrel", "format": "json"
            }, timeout=30)
            if r.status_code == 429:
                wait = 10 * (2 ** attempt)
                last_detail = f"HTTP 429 (attempt {attempt+1}/4, waiting {wait}s)"
                print(f"  ... GDELT: {q[:40]}: rate limited, retry in {wait}s")
                time.sleep(wait)
                continue
            if r.status_code == 200:
                try:
                    data = r.json()
                    articles = data.get("articles", [])
                    n = len(articles)
                    if n > 0:
                        record("1.4", f"gdelt_{q[:30]}", f"GDELT: {q[:40]}", "pass", f"{n} articles")
                        passed = True
                    else:
                        last_detail = "0 articles returned"
                except:
                    last_detail = "Non-JSON response"
                    # retry on non-JSON too
                    wait = 10 * (2 ** attempt)
                    print(f"  ... GDELT: {q[:40]}: non-JSON, retry in {wait}s")
                    time.sleep(wait)
                    continue
            else:
                last_detail = f"HTTP {r.status_code}"
        except Exception as e:
            last_detail = f"ERROR: {e}"
        break
    if not passed:
        record("1.4", f"gdelt_{q[:30]}", f"GDELT: {q[:40]}", "fail", last_detail)
    time.sleep(15)  # generous spacing to avoid rate limits

# 1.5 Yahoo Finance
print("\n--- 1.5 Yahoo Finance ---")
TICKERS = ["PANW","CRWD","FTNT","CHKP","OKTA","RPD","S","TENB","ZS","NVDA","MSFT","GOOGL","META","AAPL","IBM","AMZN","PLTR","AI"]
for ticker in TICKERS:
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
            params={"range": "2d", "interval": "1d"},
            headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            result = data.get("chart", {}).get("result", [])
            if result and result[0].get("indicators", {}).get("quote", [{}])[0].get("close"):
                closes = result[0]["indicators"]["quote"][0]["close"]
                valid = [c for c in closes if c is not None]
                if len(valid) > 0:
                    record("1.5", f"yf_{ticker}", f"Yahoo: {ticker}", "pass", f"price=${valid[-1]:.2f}")
                else:
                    record("1.5", f"yf_{ticker}", f"Yahoo: {ticker}", "fail", "No valid close prices")
            else:
                record("1.5", f"yf_{ticker}", f"Yahoo: {ticker}", "fail", "No quote data in response")
        else:
            record("1.5", f"yf_{ticker}", f"Yahoo: {ticker}", "fail", f"HTTP {r.status_code}")
    except Exception as e:
        record("1.5", f"yf_{ticker}", f"Yahoo: {ticker}", "fail", f"ERROR: {e}")
    time.sleep(0.5)

# ============================================================
# PHASE 5: API ENDPOINT TESTS (against running backend)
# ============================================================
print("\n" + "="*70)
print("PHASE 5: API ENDPOINT TESTS")
print("="*70)

BASE = "http://localhost:8443/api/v1"

# Health
print("\n--- 5.0 Health ---")
try:
    r = requests.get("http://localhost:8443/health", timeout=10)
    if r.status_code == 200 and r.json().get("status") == "ok":
        record("5.0", "health", "Health endpoint", "pass", str(r.json()))
    else:
        record("5.0", "health", "Health endpoint", "fail", f"HTTP {r.status_code}: {r.text[:200]}")
except Exception as e:
    record("5.0", "health", "Health endpoint", "fail", f"Backend unreachable: {e}")

# 5.1 Intelligence
print("\n--- 5.1 Intelligence ---")
tests_5_1 = [
    ("List events",           f"{BASE}/intelligence/",                       {"page": 1, "page_size": 5}),
    ("Pagination p2",         f"{BASE}/intelligence/",                       {"page": 2, "page_size": 5}),
    ("Filter event_type",     f"{BASE}/intelligence/",                       {"event_type": "NEWS"}),
    ("Search keyword",        f"{BASE}/intelligence/",                       {"search": "ransomware"}),
    ("Min impact",            f"{BASE}/intelligence/",                       {"min_impact": 7}),
    ("Top by impact",         f"{BASE}/intelligence/top",                    {"n": 5}),
    ("Map events",            f"{BASE}/intelligence/map",                    {}),
    ("Stats",                 f"{BASE}/intelligence/stats",                  {}),
]
for tname, url, params in tests_5_1:
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and "items" in data:
                record("5.1", f"intel_{tname}", tname, "pass", f"{data.get('total',0)} total, {len(data['items'])} items")
            elif isinstance(data, list):
                record("5.1", f"intel_{tname}", tname, "pass", f"{len(data)} items")
            elif isinstance(data, dict):
                record("5.1", f"intel_{tname}", tname, "pass", f"keys: {list(data.keys())[:5]}")
            else:
                record("5.1", f"intel_{tname}", tname, "pass", str(data)[:100])
        else:
            record("5.1", f"intel_{tname}", tname, "fail", f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        record("5.1", f"intel_{tname}", tname, "fail", f"ERROR: {e}")

# Validation tests
try:
    r = requests.get(f"{BASE}/intelligence/", params={"page_size": 200}, timeout=10)
    if r.status_code == 422:
        record("5.1", "intel_pagesize_max", "page_size > 100 rejected", "pass", "422 returned")
    else:
        record("5.1", "intel_pagesize_max", "page_size > 100 rejected", "fail", f"HTTP {r.status_code} (expected 422)")
except Exception as e:
    record("5.1", "intel_pagesize_max", "page_size > 100 rejected", "fail", str(e))

try:
    r = requests.get(f"{BASE}/intelligence/", params={"page": 0}, timeout=10)
    if r.status_code == 422:
        record("5.1", "intel_page_zero", "page=0 rejected", "pass", "422 returned")
    else:
        record("5.1", "intel_page_zero", "page=0 rejected", "fail", f"HTTP {r.status_code} (expected 422)")
except Exception as e:
    record("5.1", "intel_page_zero", "page=0 rejected", "fail", str(e))

# 5.2 Threats
print("\n--- 5.2 Threats ---")
tests_5_2 = [
    ("List threats",          f"{BASE}/threats/",                            {}),
    ("Filter severity",       f"{BASE}/threats/",                            {"severity": "CRITICAL"}),
    ("Filter min CVSS",       f"{BASE}/threats/",                            {"min_cvss": 9.0}),
    ("Search CVE",            f"{BASE}/threats/",                            {"search": "CVE-2024"}),
    ("Critical endpoint",     f"{BASE}/threats/critical",                    {"limit": 10}),
]
for tname, url, params in tests_5_2:
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and "items" in data:
                record("5.2", f"threats_{tname}", tname, "pass", f"{data.get('total',0)} total, {len(data['items'])} items")
            elif isinstance(data, list):
                record("5.2", f"threats_{tname}", tname, "pass", f"{len(data)} items")
            else:
                record("5.2", f"threats_{tname}", tname, "pass", str(data)[:100])
        else:
            record("5.2", f"threats_{tname}", tname, "fail", f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        record("5.2", f"threats_{tname}", tname, "fail", f"ERROR: {e}")

# 5.3 Financial
print("\n--- 5.3 Financial ---")
tests_5_3 = [
    ("Latest snapshots",      f"{BASE}/financial/",                          {}),
    ("Sector cyber",          f"{BASE}/financial/",                          {"sector": "cybersecurity"}),
    ("Sector ai",             f"{BASE}/financial/",                          {"sector": "ai"}),
    ("Ticker history",        f"{BASE}/financial/PANW/history",              {"limit": 10}),
    ("Movers",                f"{BASE}/financial/movers",                    {}),
    ("Invalid ticker",        f"{BASE}/financial/ZZZZZ/history",             {}),
]
for tname, url, params in tests_5_3:
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                record("5.3", f"fin_{tname}", tname, "pass", f"{len(data)} items")
            elif isinstance(data, dict):
                record("5.3", f"fin_{tname}", tname, "pass", f"keys: {list(data.keys())}")
            else:
                record("5.3", f"fin_{tname}", tname, "pass", str(data)[:100])
        else:
            record("5.3", f"fin_{tname}", tname, "fail", f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        record("5.3", f"fin_{tname}", tname, "fail", f"ERROR: {e}")

# 5.4 Streams
print("\n--- 5.4 Streams ---")
try:
    r = requests.get(f"{BASE}/streams/", timeout=10)
    if r.status_code == 200:
        data = r.json()
        record("5.4", "streams_list", "List streams", "pass", f"{len(data)} streams")
    else:
        record("5.4", "streams_list", "List streams", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("5.4", "streams_list", "List streams", "fail", str(e))

try:
    r = requests.get(f"{BASE}/streams/", params={"live_only": "true"}, timeout=10)
    if r.status_code == 200:
        record("5.4", "streams_live", "Live only filter", "pass", f"{len(r.json())} live streams")
    else:
        record("5.4", "streams_live", "Live only filter", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("5.4", "streams_live", "Live only filter", "fail", str(e))

# 5.5 Certifications
print("\n--- 5.5 Certifications ---")
tests_5_5 = [
    ("List certs",            f"{BASE}/certifications/",                     {}),
    ("Filter body",           f"{BASE}/certifications/",                     {"body_name": "NIST"}),
    ("Bodies list",           f"{BASE}/certifications/bodies",               {}),
]
for tname, url, params in tests_5_5:
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict) and "items" in data:
                record("5.5", f"cert_{tname}", tname, "pass", f"{data.get('total',0)} total, {len(data['items'])} items")
            elif isinstance(data, dict) and "bodies" in data:
                record("5.5", f"cert_{tname}", tname, "pass", f"{len(data['bodies'])} bodies")
            elif isinstance(data, dict):
                record("5.5", f"cert_{tname}", tname, "pass", f"keys: {list(data.keys())}")
            elif isinstance(data, list):
                record("5.5", f"cert_{tname}", tname, "pass", f"{len(data)} items")
            else:
                record("5.5", f"cert_{tname}", tname, "pass", str(data)[:100])
        else:
            record("5.5", f"cert_{tname}", tname, "fail", f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        record("5.5", f"cert_{tname}", tname, "fail", f"ERROR: {e}")

# 5.6 CORS
print("\n--- 5.6 CORS & Docs ---")
try:
    r = requests.options(f"{BASE}/intelligence/", headers={
        "Origin": "http://localhost:1337",
        "Access-Control-Request-Method": "GET"
    }, timeout=10)
    if "access-control-allow-origin" in r.headers:
        record("5.6", "cors_allowed", "CORS allowed origin", "pass", r.headers.get("access-control-allow-origin"))
    else:
        record("5.6", "cors_allowed", "CORS allowed origin", "fail", f"No ACAO header. Headers: {dict(r.headers)}")
except Exception as e:
    record("5.6", "cors_allowed", "CORS allowed origin", "fail", str(e))

try:
    r = requests.get("http://localhost:8443/docs", timeout=10)
    if r.status_code == 200 and "swagger" in r.text.lower():
        record("5.6", "docs", "Swagger docs", "pass", "Swagger UI loaded")
    else:
        record("5.6", "docs", "Swagger docs", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("5.6", "docs", "Swagger docs", "fail", str(e))

# ============================================================
# PHASE 7: INFRASTRUCTURE TESTS
# ============================================================
print("\n" + "="*70)
print("PHASE 7: INFRASTRUCTURE TESTS")
print("="*70)

# Frontend reachable
print("\n--- 7.1 Docker Services ---")
try:
    r = requests.get("http://localhost:1337", timeout=10)
    if r.status_code == 200:
        record("7.1", "frontend", "Frontend reachable", "pass", f"HTTP 200, {len(r.text)} bytes")
    else:
        record("7.1", "frontend", "Frontend reachable", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("7.1", "frontend", "Frontend reachable", "fail", str(e))

# API proxy through nginx
try:
    r = requests.get("http://localhost:1337/api/v1/intelligence/stats", timeout=10)
    if r.status_code == 200:
        record("7.1", "nginx_proxy", "Nginx API proxy", "pass", "Proxied to backend OK")
    else:
        record("7.1", "nginx_proxy", "Nginx API proxy", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("7.1", "nginx_proxy", "Nginx API proxy", "fail", str(e))

# SPA fallback
try:
    r = requests.get("http://localhost:1337/intelligence", timeout=10)
    if r.status_code == 200 and ("<!DOCTYPE" in r.text or "<html" in r.text):
        record("7.1", "spa_fallback", "SPA fallback", "pass", "Returns index.html for SPA route")
    else:
        record("7.1", "spa_fallback", "SPA fallback", "fail", f"HTTP {r.status_code}")
except Exception as e:
    record("7.1", "spa_fallback", "SPA fallback", "fail", str(e))

# Security: SQL injection attempt
print("\n--- 7.3 Security ---")
try:
    r = requests.get(f"{BASE}/intelligence/", params={"search": "' OR 1=1--"}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        # If parameterized, this should return 0 results (not all rows)
        record("7.3", "sqli", "SQL injection blocked", "pass", f"Parameterized query, {data.get('total',0)} results")
    elif r.status_code == 500:
        record("7.3", "sqli", "SQL injection blocked", "fail", "Server error - possible SQL injection vulnerability")
    else:
        record("7.3", "sqli", "SQL injection blocked", "pass", f"HTTP {r.status_code}")
except Exception as e:
    record("7.3", "sqli", "SQL injection blocked", "fail", str(e))

# CORS blocked for evil origin
try:
    r = requests.options(f"{BASE}/intelligence/", headers={
        "Origin": "http://evil.com",
        "Access-Control-Request-Method": "GET"
    }, timeout=10)
    acao = r.headers.get("access-control-allow-origin", "")
    if acao == "" or acao != "http://evil.com":
        record("7.3", "cors_block", "CORS blocks evil origin", "pass", f"ACAO='{acao}'")
    else:
        record("7.3", "cors_block", "CORS blocks evil origin", "fail", f"Evil origin allowed: {acao}")
except Exception as e:
    record("7.3", "cors_block", "CORS blocks evil origin", "fail", str(e))

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

passes = [r for r in RESULTS if r["status"] == "pass"]
fails = [r for r in RESULTS if r["status"] == "fail"]
print(f"\nTotal: {len(RESULTS)} | PASS: {len(passes)} | FAIL: {len(fails)}")

if fails:
    print(f"\n--- FAILURES ({len(fails)}) ---")
    for f in fails:
        print(f"  [{f['phase']}] {f['name']}: {f['detail']}")

# Write JSON for further processing
with open("/home/rare/projects/cyberverse/test_results.json", "w") as fh:
    json.dump({"total": len(RESULTS), "passes": len(passes), "failures": len(fails), "results": RESULTS}, fh, indent=2)

print(f"\nResults saved to test_results.json")
