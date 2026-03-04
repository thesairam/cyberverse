import sys, asyncio, random, uuid
from datetime import datetime, timezone, timedelta
sys.path.insert(0, '/app')
from app.database import AsyncSessionLocal
from app.models.intelligence import FinancialSnapshot

# Realistic price data as of early 2026
STOCKS = [
    ("PANW",  "Palo Alto Networks",   "cybersecurity", 185.40,  2.1),
    ("CRWD",  "CrowdStrike",          "cybersecurity", 362.80,  1.8),
    ("FTNT",  "Fortinet",             "cybersecurity",  71.20, -0.9),
    ("CHKP",  "Check Point Software", "cybersecurity", 198.60,  0.4),
    ("OKTA",  "Okta",                 "cybersecurity",  95.30, -1.5),
    ("RPD",   "Rapid7",               "cybersecurity",  42.10, -0.3),
    ("S",     "SentinelOne",          "cybersecurity",  22.80,  3.2),
    ("CYBR",  "CyberArk",             "cybersecurity", 312.50,  1.1),
    ("ZS",    "Zscaler",              "cybersecurity", 198.70,  0.7),
    ("NVDA",  "NVIDIA",               "ai",           128.40,  4.5),
    ("MSFT",  "Microsoft",            "ai",           420.60,  0.8),
    ("GOOGL", "Alphabet",             "ai",           196.20,  1.2),
    ("META",  "Meta Platforms",       "ai",           611.80,  2.3),
    ("AAPL",  "Apple",                "ai",           237.30, -0.4),
    ("IBM",   "IBM",                  "ai",           238.90,  0.6),
    ("AMZN",  "Amazon",               "ai",           216.40,  1.7),
    ("PLTR",  "Palantir",             "ai",            78.20,  5.1),
    ("AI",    "C3.ai",                "ai",            34.60, -2.1),
]

MCAPS = {
    "PANW": 57e9,  "CRWD": 87e9,  "FTNT": 52e9,  "CHKP": 18e9,
    "OKTA": 12e9,  "RPD": 2.5e9,  "S": 6.5e9,   "CYBR": 12e9,
    "ZS":   27e9,  "NVDA": 3.1e12,"MSFT": 3.1e12,"GOOGL": 2.4e12,
    "META": 1.5e12,"AAPL": 3.6e12,"IBM": 220e9,  "AMZN": 2.3e12,
    "PLTR": 165e9, "AI":   7.2e9,
}

async def seed():
    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)
        rows = []
        for ticker, name, sector, price, chg in STOCKS:
            noise = random.uniform(-0.5, 0.5)
            p = round(price * (1 + noise/100), 2)
            rows.append(FinancialSnapshot(
                id=uuid.uuid4(),
                ticker=ticker,
                company_name=name,
                sector=sector,
                price=p,
                open_price=round(p * 0.998, 2),
                high=round(p * 1.012, 2),
                low=round(p * 0.989, 2),
                volume=random.randint(1_000_000, 80_000_000),
                market_cap=MCAPS.get(ticker),
                pe_ratio=round(random.uniform(18, 65), 1),
                change_pct=round(chg + random.uniform(-0.3, 0.3), 2),
                currency="USD",
                exchange="NASDAQ",
                snapshot_at=now,
            ))
        session.add_all(rows)
        await session.commit()
        print(f"Seeded {len(rows)} financial snapshots")

asyncio.run(seed())
