import asyncio, sys
sys.path.insert(0, '/app')
from app.database import AsyncSessionLocal

async def run():
    from app.collectors.rss_collector import RSSCollector
    from app.collectors.cve_collector import CVECollector
    from app.collectors.financial_collector import FinancialCollector
    from app.normalizer import upsert_events, upsert_threats, insert_financial

    print("=== RSS ===", flush=True)
    try:
        rows = await RSSCollector().collect()
        print(f"  fetched {len(rows)}", flush=True)
        async with AsyncSessionLocal() as s:
            n = await upsert_events(s, rows)
            print(f"  saved {n}", flush=True)
    except Exception as e:
        print(f"  RSS ERROR: {e}", flush=True)

    print("=== CVE ===", flush=True)
    try:
        rows = await CVECollector().collect()
        print(f"  fetched {len(rows)}", flush=True)
        async with AsyncSessionLocal() as s:
            n = await upsert_threats(s, rows)
            print(f"  saved {n}", flush=True)
    except Exception as e:
        print(f"  CVE ERROR: {e}", flush=True)

    print("=== Financial ===", flush=True)
    try:
        rows = await FinancialCollector().collect()
        print(f"  fetched {len(rows)}", flush=True)
        async with AsyncSessionLocal() as s:
            n = await insert_financial(s, rows)
            print(f"  saved {n}", flush=True)
    except Exception as e:
        print(f"  Financial ERROR: {e}", flush=True)

asyncio.run(run())
