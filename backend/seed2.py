import asyncio, sys, os
sys.path.insert(0, '/app')
os.environ.setdefault('DATABASE_URL', 'postgresql+asyncpg://cyberverse:cyberverse@postgres:5432/cyberverse')

async def main():
    from app.database import init_db, AsyncSessionLocal
    from app.collectors.rss_collector import RSSCollector
    from app.collectors.cve_collector import CVECollector
    from app.collectors.gdelt_collector import GDELTCollector
    from app.normalizer import upsert_events, upsert_threats

    await init_db()

    # RSS with new/EU sources
    print("=== RSS Collector ===")
    rss = RSSCollector()
    rss_events = await rss.collect()
    print(f"Fetched {len(rss_events)} RSS events")
    if rss_events:
        async with AsyncSessionLocal() as session:
            saved = await upsert_events(session, rss_events)
            await session.commit()
        print(f"Saved {saved} new events")
        for e in rss_events:
            t = e.get('title','').lower()
            if any(kw in t for kw in ['odido','telecom','netherland','dutch','ddos','ransomware']):
                print(f"  [HIT] {e['source_name']}: {e['title'][:80]}")

    # GDELT with Odido + EU queries
    print("\n=== GDELT Collector ===")
    gdelt = GDELTCollector()
    gdelt_events = await gdelt.collect()
    print(f"Fetched {len(gdelt_events)} GDELT events")
    if gdelt_events:
        async with AsyncSessionLocal() as session:
            saved = await upsert_events(session, gdelt_events)
            await session.commit()
        print(f"Saved {saved} new events")
        for e in gdelt_events:
            t = e.get('title','').lower()
            if any(kw in t for kw in ['odido','telecom','netherland','dutch','ddos']):
                print(f"  [EU HIT] {e['source_name']}: {e['title'][:80]}")

    # CVE refresh
    print("\n=== CVE Collector ===")
    cve = CVECollector()
    cve_events = await cve.collect()
    print(f"Fetched {len(cve_events)} CVEs")
    if cve_events:
        async with AsyncSessionLocal() as session:
            saved = await upsert_threats(session, cve_events)
            await session.commit()
        print(f"Saved {saved} new threats")

    # Final count
    from sqlalchemy import text
    async with AsyncSessionLocal() as session:
        r = await session.execute(text("SELECT COUNT(*) FROM intelligenceevents"))
        total = r.scalar()
        print(f"\nTotal events in DB: {total}")

asyncio.run(main())
