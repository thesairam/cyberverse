import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any
import httpx
from app.collectors.base import BaseCollector

logger = logging.getLogger(__name__)

WATCHLIST: list[tuple[str, str, str]] = [
    ("PANW",  "Palo Alto Networks",    "cybersecurity"),
    ("CRWD",  "CrowdStrike",           "cybersecurity"),
    ("FTNT",  "Fortinet",              "cybersecurity"),
    ("CHKP",  "Check Point Software",  "cybersecurity"),
    ("OKTA",  "Okta",                  "cybersecurity"),
    ("RPD",   "Rapid7",                "cybersecurity"),
    ("S",     "SentinelOne",           "cybersecurity"),
    ("TENB",  "Tenable Holdings",      "cybersecurity"),
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
    ("ASML",  "ASML Holding",           "semiconductor"),
    ("BFIT.AS", "Basic-Fit",            "fitness"),
]

# Yahoo v8 chart API — lighter than v10 quoteSummary, less prone to 429s
# Try both query1 and query2 endpoints for resilience
CHART_APIS = [
    "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
    "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}",
]
# Rotate User-Agents to reduce fingerprinting
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

MAX_RETRIES = 3
RETRY_BACKOFF = 3  # seconds, doubles each retry


def _fetch_chart(ticker: str, company: str, sector: str) -> dict[str, Any] | None:
    """Fetch price data from Yahoo v8 chart API with retry on 429."""
    import random
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    for attempt in range(MAX_RETRIES):
        api_url = CHART_APIS[attempt % len(CHART_APIS)]  # alternate between endpoints
        try:
            with httpx.Client(headers=headers, follow_redirects=True, timeout=15.0) as client:
                resp = client.get(
                    api_url.format(ticker=ticker),
                    params={"range": "2d", "interval": "1d"},
                )

            if resp.status_code == 429:
                wait = RETRY_BACKOFF * (2 ** attempt)
                logger.warning("[financial] %s: 429 rate-limited, retry %d in %ds", ticker, attempt + 1, wait)
                time.sleep(wait)
                continue

            if resp.status_code != 200:
                logger.warning("[financial] %s: HTTP %d", ticker, resp.status_code)
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
                "market_cap":   meta.get("marketCap"),
                "pe_ratio":     None,
                "currency":     meta.get("currency", "USD"),
                "exchange":     meta.get("exchangeName"),
                "change_pct":   change_pct,
                "snapshot_at":  datetime.now(timezone.utc),
            }
        except Exception as exc:
            logger.warning("[financial] %s error (attempt %d): %s", ticker, attempt + 1, exc)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))

    logger.error("[financial] %s: all %d retries exhausted", ticker, MAX_RETRIES)
    return None


class FinancialCollector(BaseCollector):
    name = "financial"

    async def collect(self) -> list[dict[str, Any]]:
        loop = asyncio.get_event_loop()
        results: list[dict[str, Any]] = []
        for t, n, s in WATCHLIST:
            r = await loop.run_in_executor(None, _fetch_chart, t, n, s)
            if r is not None:
                results.append(r)
            await asyncio.sleep(1.0)  # pacing between tickers to avoid throttle
        logger.info("[financial] fetched %d/%d tickers", len(results), len(WATCHLIST))
