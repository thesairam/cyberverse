import asyncio, sys, os
sys.path.insert(0, '/app')
os.environ.setdefault('DATABASE_URL', 'postgresql+asyncpg://cyberverse:cyberverse@postgres:5432/cyberverse')

# Country name → (lat, lon) approx centroid
COUNTRY_COORDS = {
    "United States": (37.09, -95.71), "China": (35.86, 104.19), "Russia": (61.52, 105.32),
    "Germany": (51.16, 10.45), "United Kingdom": (55.37, -3.43), "France": (46.22, 2.21),
    "Japan": (36.20, 138.25), "South Korea": (35.90, 127.76), "India": (20.59, 78.96),
    "Australia": (-25.27, 133.77), "Canada": (56.13, -106.34), "Brazil": (-14.23, -51.92),
    "Netherlands": (52.13, 5.29), "Norway": (60.47, 8.46), "Sweden": (60.12, 18.64),
    "Finland": (61.92, 25.74), "Denmark": (56.26, 9.50), "Belgium": (50.50, 4.46),
    "Switzerland": (46.81, 8.22), "Austria": (47.51, 14.55), "Spain": (40.46, -3.74),
    "Italy": (41.87, 12.56), "Poland": (51.91, 19.14), "Ukraine": (48.37, 31.16),
    "Israel": (31.04, 34.85), "Iran": (32.42, 53.68), "Turkey": (38.96, 35.24),
    "Taiwan": (23.69, 120.96), "Singapore": (1.35, 103.81), "Malaysia": (4.21, 101.97),
    "Indonesia": (-0.78, 113.92), "Thailand": (15.87, 100.99), "Vietnam": (14.05, 108.27),
    "Philippines": (12.87, 121.77), "Pakistan": (30.37, 69.34), "Bangladesh": (23.68, 90.35),
    "Nigeria": (9.08, 8.67), "South Africa": (-30.55, 22.93), "Kenya": (-0.02, 37.90),
    "Egypt": (26.82, 30.80), "Saudi Arabia": (23.88, 45.07), "UAE": (23.42, 53.84),
    "Mexico": (23.63, -102.55), "Argentina": (-38.41, -63.61), "Colombia": (4.57, -74.29),
    "Cyprus": (35.12, 33.42), "Greece": (39.07, 21.82), "Romania": (45.94, 24.96),
    "Czech Republic": (49.81, 15.47), "Hungary": (47.16, 19.50), "Portugal": (39.39, -8.22),
    "New Zealand": (-40.90, 174.88), "Hong Kong": (22.39, 114.10), "Luxembourg": (49.81, 6.12),
    "Ireland": (53.41, -8.24), "Iceland": (64.96, -19.02),
}

async def main():
    from app.database import init_db, AsyncSessionLocal
    from sqlalchemy import text

    await init_db()

    # 1. Backfill lat/lon from country name for existing events
    async with AsyncSessionLocal() as session:
        # Build a big CASE statement
        when_clauses = "\n".join(
            f"WHEN country = '{name}' THEN {lat}"
            for name, (lat, lon) in COUNTRY_COORDS.items()
        )
        when_lon_clauses = "\n".join(
            f"WHEN country = '{name}' THEN {lon}"
            for name, (lat, lon) in COUNTRY_COORDS.items()
        )
        sql = f"""
            UPDATE intelligence_events
            SET
                latitude = CASE {when_clauses} ELSE latitude END,
                longitude = CASE {when_lon_clauses} ELSE longitude END
            WHERE country IS NOT NULL
              AND latitude IS NULL
        """
        result = await session.execute(text(sql))
        await session.commit()
        print(f"Geo-backfilled {result.rowcount} events with lat/lon from country name")

        r = await session.execute(text("SELECT COUNT(*) FROM intelligence_events WHERE latitude IS NOT NULL"))
        print(f"Total events now with lat/lon: {r.scalar()}")

    # 2. Run cert_collector
    print("\n=== Cert Collector ===")
    from app.collectors.cert_collector import CertCollector
    from app.normalizer import upsert_certifications

    cert = CertCollector()
    cert_records = await cert.collect()
    print(f"Fetched {len(cert_records)} cert updates")
    if cert_records:
        async with AsyncSessionLocal() as session:
            saved = await upsert_certifications(session, cert_records)
            await session.commit()
        print(f"Saved {saved} cert updates")
        for c in cert_records[:10]:
            print(f"  [{c['body_name']}] {c['title'][:80]}")

asyncio.run(main())
