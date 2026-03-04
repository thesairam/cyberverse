import asyncio
from datetime import datetime, timezone
from typing import Any
import yfinance as yf
from app.collectors.base import BaseCollector

WATCHLIST: list[tuple[str, str, str]] = [
    ("PANW",  "Palo Alto Networks",    "cybersecurity"),
    ("CRWD",  "CrowdStrike",           "cybersecurity"),
    ("FTNT",  "Fortinet",              "cybersecurity"),
    ("CHKP",  "Check Point Software",  "cybersecurity"),
    ("OKTA",  "Okta",                  "cybersecurity"),
    ("RPD",   "Rapid7",                "cybersecurity"),
    ("S",     "SentinelOne",           "cybersecurity"),
    ("CYBR",  "CyberArk",              "cybersecurity"),
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


def _fetch_ticker(ticker: str, company: str, sector: str) -> dict[str, Any] | None:
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if hist.empty:
            return None
        latest = hist.iloc[-1]
        prev   = hist.iloc[-2] if len(hist) > 1 else latest
        price      = float(latest["Close"])
        prev_close = float(prev["Close"])
        change_pct = round((price - prev_close) / prev_close * 100, 4) if prev_close else None
        return {
            "ticker":       ticker,
            "company_name": company,
            "sector":       sector,
            "price":        round(price, 4),
            "open_price":   float(latest.get("Open", price)),
            "high":         float(latest.get("High", price)),
            "low":          float(latest.get("Low", price)),
            "volume":       int(latest.get("Volume", 0)),
            "market_cap":   None,
            "currency":     "USD",
            "exchange":     None,
            "change_pct":   change_pct,
            "snapshot_at":  datetime.now(timezone.utc),
        }
    except Exception as exc:
        print(f"[Financial] {ticker} error: {exc}")
        return None


class FinancialCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(None, _fetch_ticker, t, n, s) for t, n, s in WATCHLIST]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
