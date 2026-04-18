# CyberVerse — Real-Time Global Intelligence Aggregator

## Overview
A full-stack cybersecurity & AI intelligence dashboard that continuously collects, normalizes, and visualizes worldwide threat data, news, market trends, and policy updates from free open-source feeds into a unified real-time analytics platform.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue 3 (Composition API) + TypeScript, Pinia, Tailwind CSS, Chart.js, Leaflet, Vite |
| **Backend** | FastAPI (async Python), SQLAlchemy 2.0 (async), APScheduler, VADER Sentiment |
| **Database** | PostgreSQL 16 (asyncpg driver, Alembic migrations) |
| **Infra** | Docker Compose, Nginx reverse proxy, multi-stage builds |

---

## Architecture

```
DATA SOURCES (free, no auth)
  │  RSS (15+ feeds) · GDELT · NVD/CVE · yfinance · YouTube · Standards Bodies
  ▼
BACKEND (FastAPI)
  │  6 Collectors → Normalizer (sentiment + impact scoring) → PostgreSQL
  │  APScheduler: Intel every 15m, CVE every 30m, Financial every 60m
  ▼
5 TABLES: intelligence_events · threat_indicators · financial_snapshots
          live_streams · certification_updates
  ▼
REST API (/api/v1/*)
  │  intelligence · threats · financial · streams · certifications
  ▼
FRONTEND (Vue 3 SPA)
  │  7 views, 4 Pinia stores, Axios API service
  ▼
NGINX → serves SPA, proxies /api/* to backend
```

---

## 6 Data Collectors

| Collector | Source | Schedule | Data |
|---|---|---|---|
| **RSS** | 15+ feeds (Hacker News, Dark Reading, Krebs, CISA, TechCrunch AI, etc.) | 15 min | News, alerts, policy |
| **GDELT** | GDELT 2.0 DOC API (5 queries, 250 articles/cycle) | 15 min | Geotagged global news |
| **CVE** | NVD REST API v2 (last 48h, 100/cycle) | 30 min | CVE ID, CVSS, severity, CWE, CPE |
| **Financial** | yfinance (18 tickers: PANW, CRWD, NVDA, MSFT, etc.) | 60 min | Price, volume, market cap, P/E |
| **YouTube** | YouTube Data API v3 (optional, needs API key) | 15 min | Live streams, conferences, CTFs |
| **Certifications** | 10 standards bodies (NIST, ENISA, OWASP, ISC2, etc.) | 15 min | Standards updates, revisions, alerts |

---

## 5 Database Tables

- **intelligence_events** — Upsert on `source_url`; stores sentiment (-1 to +1), impact (0-10), geo coords, JSONB extra
- **threat_indicators** — Upsert on `indicator_id` (CVE-YYYY-NNNN); CVSS score, severity, affected products, CWE IDs
- **financial_snapshots** — Time-series inserts; ticker, price, volume, market cap, % change
- **live_streams** — Upsert on `video_id`; is_live flag, viewer count, channel info
- **certification_updates** — Body name, standard ID, update type (RELEASE/REVISION/ALERT), region

---

## API Endpoints

| Router | Endpoints |
|---|---|
| **Intelligence** | `GET /` (paginated, filtered), `/top` (by impact), `/map` (geotagged), `/stats` (aggregates) |
| **Threats** | `GET /` (paginated, filtered by severity/CVSS), `/critical` (top 10) |
| **Financial** | `GET /` (latest per ticker), `/{ticker}/history`, `/movers` (gainers/losers) |
| **Streams** | `GET /` (sorted by live status & viewers) |
| **Certifications** | `GET /` (filtered by body/region/type), `/bodies` (list all) |

---

## 7 Frontend Views

| View | Features |
|---|---|
| **Dashboard** | 4 KPI cards, event breakdown chart, top impact events, critical CVEs, market movers |
| **Intelligence** | Searchable/filterable feed with pagination, event type & category filters, impact slider |
| **Threat Intel** | CVE table with severity badges, CVSS color-coding, clickable references |
| **World Map** | Leaflet interactive map, geotagged events, impact-based color legend |
| **Financial** | Stock grid cards (price, % change, volume), market cap table, sector filters |
| **Live Streams** | YouTube live/VOD cards, LIVE badge (pulsing), viewer count, "live only" toggle |
| **Certifications** | Standards body pill filters, region/type filters, paginated update cards |

---

## Deployment Ports

| Service | Port | Purpose |
|---|---|---|
| Frontend | `1337` | "leet" — Vue SPA via Nginx |
| Backend | `8443` | Secure API port — FastAPI |
| PostgreSQL | `5432` | Database |
| pgAdmin | `5050` | DB admin (dev profile only) |

---

## Key Design Decisions
- **All async I/O** (database, HTTP, schedulers)
- **Upsert idempotency** prevents duplicate records
- **VADER sentiment** + keyword-heuristic impact scoring (no ML model dependency)
- **Graceful degradation** — one collector failing doesn't block others
- **Dark cyber theme** (gray-950 + teal/cyan accents)
- **Polling-based** updates (REST, no WebSocket/SSE)

IMPORTANT!

If I am asking to fix a bug or append a feature, ensure to work only that specific task and never break/build anything else or soemthing that affects other features. 