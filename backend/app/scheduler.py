"""APScheduler background jobs."""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import get_settings
from app.database import AsyncSessionLocal

_scheduler = AsyncIOScheduler(timezone="UTC")
_settings = get_settings()


async def _run_intelligence_collectors() -> None:
    from app.collectors import RSSCollector, GDELTCollector, CertCollector, GoogleNewsCollector
    from app.normalizer import upsert_events, upsert_certifications
    async with AsyncSessionLocal() as session:
        for Cls in (RSSCollector, GDELTCollector, GoogleNewsCollector):
            try:
                rows = await Cls().collect()
                n = await upsert_events(session, rows)
                print(f"[Scheduler] {Cls.__name__}: upserted {n}")
            except Exception as e:
                print(f"[Scheduler] {Cls.__name__} failed: {e}")
        try:
            rows = await CertCollector().collect()
            n = await upsert_certifications(session, rows)
            print(f"[Scheduler] CertCollector: upserted {n}")
        except Exception as e:
            print(f"[Scheduler] CertCollector failed: {e}")


async def _run_cve_collector() -> None:
    from app.collectors import CVECollector
    from app.normalizer import upsert_threats
    async with AsyncSessionLocal() as session:
        try:
            rows = await CVECollector().collect()
            n = await upsert_threats(session, rows)
            print(f"[Scheduler] CVECollector: upserted {n}")
        except Exception as e:
            print(f"[Scheduler] CVECollector failed: {e}")


async def _run_financial_collector() -> None:
    from app.collectors import FinancialCollector
    from app.normalizer import insert_financial
    async with AsyncSessionLocal() as session:
        try:
            rows = await FinancialCollector().collect()
            n = await insert_financial(session, rows)
            print(f"[Scheduler] FinancialCollector: inserted {n}")
        except Exception as e:
            print(f"[Scheduler] FinancialCollector failed: {e}")


def start_scheduler() -> None:
    interval = _settings.COLLECT_INTERVAL_MINUTES
    fin_interval = _settings.FINANCIAL_INTERVAL_MINUTES
    _scheduler.add_job(_run_intelligence_collectors, "interval", minutes=interval, id="intel_collect", replace_existing=True)
    _scheduler.add_job(_run_cve_collector,           "interval", minutes=30,         id="cve_collect",   replace_existing=True)
    _scheduler.add_job(_run_financial_collector,     "interval", minutes=fin_interval, id="fin_collect", replace_existing=True)
    _scheduler.start()
    print(f"[Scheduler] Started — intel={interval}m cve=30m financial={fin_interval}m")


def stop_scheduler() -> None:
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
