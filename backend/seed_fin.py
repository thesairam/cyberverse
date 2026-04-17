"""Seed financial data using REAL prices from Yahoo Finance v8 chart API.
Uses direct HTTP calls to the chart endpoint to avoid yfinance rate limits.
"""
import sys, asyncio, uuid, time
from datetime import datetime, timezone
sys.path.insert(0, '/app')
import httpx
from app.database import AsyncSessionLocal
from app.models.intelligence import FinancialSnapshot

WATCHLIST = [
    ("PANW",  "Palo Alto Networks",   "cybersecurity"),
    ("CRWD",  "CrowdStrike",          "cybersecurity"),
    ("FTNT",  "Fortinet",             "cybersecurity"),
    ("CHKP",  "Check Point Software", "cybersecurity"),
    ("OKTA",  "Okta",                 "cybersecurity"),
    ("RPD",   "Rapid7",               "cybersecurity"),
    ("S",     "SentinelOne",          "cybersecurity"),
    ("CYBR",  "CyberArk",             "cybersecurity"),
    ("ZS",    "Zscaler",              "cybersecurity"),
    ("NVDA",  "NVIDIA",               "ai"),
    ("MSFT",  "Microsoft",            "ai"),
    ("GOOGL", "Alphabet",             "ai"),
    ("META",  "Meta Platforms",       "ai"),
    ("AAPL",  "Apple",                "ai"),
    ("IBM",   "IBM",                  "ai"),
    ("AMZN",  "Amazon",               "ai"),
    ("PLTR",  "Palantir",             "ai"),
    ("AI",    "C3.ai",                "ai"),
]

CHART_API = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _fetch_chart(client: httpx.Client, ticker: str, company: str, sector: str) -> dict | None:
    try:
        resp = client.get(
            CHART_API.format(ticker=ticker),
            params={"range": "2d", "interval": "1d"},
        )
        if resp.status_code != 200:
            print(f"  {ticker}: HTTP {resp.status_code}")
            return None
        result = resp.json()["chart"]["result"][0]
        meta = result.get("meta", {})
        quote = result["indicators"]["quote"][0]
        closes = quote.get("close", [])
        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        volumes = quote.get("volume", [])
        if not closes or closes[-1] is None:
            print(f"  {ticker}: no close data")
            return None
        price = round(closes[-1], 2)
        prev_close = closes[-2] if len(closes) > 1 and closes[-2] is not None else price
        change_pct = round((price - prev_close) / prev_close * 100, 4) if prev_close else 0.0
        return {
            "ticker": ticker,
            "company_name": company,
            "sector": sector,
            "price": price,
            "open_price": round(opens[-1], 2) if opens and opens[-1] is not None else price,
            "high": round(highs[-1], 2) if highs and highs[-1] is not None else price,
            "low": round(lows[-1], 2) if lows and lows[-1] is not None else price,
            "volume": int(volumes[-1]) if volumes and volumes[-1] is not None else 0,
            "market_cap": None,
            "pe_ratio": None,
            "change_pct": change_pct,
            "currency": meta.get("currency", "USD"),
            "exchange": meta.get("exchangeName", "NASDAQ"),
        }
    except Exception as exc:
        print(f"  {ticker}: error — {exc}")
        return None


async def seed():
    now = datetime.now(timezone.utc)
    print(f"[seed_fin] Fetching real prices from Yahoo Finance chart API...")
    snapshots = []
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=15.0) as client:
        for ticker, company, sector in WATCHLIST:
            data = _fetch_chart(client, ticker, company, sector)
            if data is None:
                continue
            snapshots.append(FinancialSnapshot(
                id=uuid.uuid4(),
                snapshot_at=now,
                **data,
            ))
            print(f"  {ticker}: ${data['price']} ({data['change_pct']:+.2f}%)")
            time.sleep(0.5)

    if not snapshots:
        print("[seed_fin] No snapshots built — check output above")
        return

    async with AsyncSessionLocal() as session:
        session.add_all(snapshots)
        await session.commit()
        print(f"[seed_fin] Seeded {len(snapshots)} financial snapshots with REAL data")

asyncio.run(seed())
