import asyncio
from datetime import datetime, timezone
from typing import Any
import httpx
from app.collectors.base import BaseCollector

WATCHLIST: list[tuple[str, str, str]] = [
    ("PANW",  "Palo Alto Networks",    "cybersecurity"),
    ("CRWD",  "CrowdStrike",           "cybersecurity"),
    ("FTNT",  "Fortinet",              "cybersecurity"),
    ("CHKP",  "Check Point Software",  "cybersecurity"),
    ("OKTA",  "Okta",                  "cybersecurity"),
    ("RPD",   "Rapid7",                "cybersecurity"),
    ("S",     "SentinelOne",           "cybersecurity"),
    ("TENB",  "Tenable Holdings",     "cybersecurity"),
    ("ZS",    "Zscaler",               "cybersecurity"),
    ("NVDA",  "NVIDIA",                "ai"),
    ("MSFT",  "Microsoft",             "ai"),
    ("GOOGL", "Alphabet",              "ai"),
    ("META",  "Meta Platforms",        "ai"),
    ("AAPL",  "Apple",                 "ai"),
    ("IBM",   "IBM",                   "ai"),
    ("AMZN",  "Amazon",               "ai"),
    ("PLTR",  "Palantir",              "ai"),
    ("AI",    "C3.ai",                 "ai"),
]

CHART_API = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def _fetch_chart(ticker: str, company: str, sector: str) -> dict[str, Any] | None:
    """Fetch real price data from Yahoo Finance v8 chart API."""
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=15.0) as client:
            resp = client.get(
                CHART_API.format(ticker=ticker),
                params={"range": "2d", "interval": "1d"},
            )
        if resp.status_code != 200:
            print(f"[Financial] {ticker}: HTTP {resp.status_code}")
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
            return None
        price = float(closes[-1])
        prev_close = closes[-2] if len(closes) > 1 and closes[-2] is not None else price
        change_pct = round((price - prev_close) / prev_close * 100, 4) if prev_close else None
        return {
            "ticker":       ticker,
            "company_name": company,
            "sector":       sector,
            "price":        round(price, 4),
            "open_price":   round(opens[-1], 4) if opens and opens[-1] is not None else round(price, 4),
            "high":         round(highs[-1], 4) if highs and highs[-1] is not None else round(price, 4),
            "low":          round(lows[-1], 4) if lows and lows[-1] is not None else round(price, 4),
            "volume":       int(volumes[-1]) if volumes and volumes[-1] is not None else 0,
            "market_cap":   None,
            "pe_ratio":     None,
            "currency":     meta.get("currency", "USD"),
            "exchange":     meta.get("exchangeName"),
            "change_pct":   change_pct,
            "snapshot_at":  datetime.now(timezone.utc),
        }
    except Exception as exc:
        print(f"[Financial] {ticker} error: {exc}")
        return None


class FinancialCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        results: list[dict[str, Any]] = []
        for t, n, s in WATCHLIST:
            r = await loop.run_in_executor(None, _fetch_chart, t, n, s)
            if r is not None:
                results.append(r)
            await asyncio.sleep(0.5)  # gentle pacing
        return results
