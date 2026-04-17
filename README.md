# CyberVerse — Real-Time Global Intelligence Aggregator

A full-stack dashboard for Cybersecurity & AI intelligence — aggregating news, CVEs, financial data, live streams, and certification updates in real-time.

## Stack

| Layer     | Technology |
|-----------|-----------|
| Backend   | Python 3.12, FastAPI, SQLAlchemy 2 (async), APScheduler |
| Database  | PostgreSQL 16 |
| Frontend  | Vue 3 + TypeScript, Vite, Pinia, Tailwind CSS |
| Map       | Leaflet.js |
| Charts    | Chart.js |
| Deploy    | Docker Compose + Nginx |

## Quick Start (Docker — recommended)

```bash
cd /home/rare/projects/cyberverse
cp backend/.env.example backend/.env
docker compose up --build
```

- **Dashboard** → http://localhost:1337
- **API docs**  → http://localhost:8443/docs
- **pgAdmin**   → `docker compose --profile dev up` → http://localhost:5050

## Local Development

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit DATABASE_URL in .env to point to your local Postgres
alembic upgrade head
uvicorn app.main:app --reload --port 8443
```

### Frontend
```bash
cd frontend
npm install
npm run dev          # → http://localhost:5173
```

## Port Details

| Service | Docker Service | Host Port | Container Port | Access | Purpose |
|---------|----------------|-----------|----------------|--------|---------|
| Frontend (Nginx) | `frontend` | `1337` | `80` | http://localhost:1337 | Serves Vue SPA and proxies `/api/*` |
| Backend (FastAPI) | `backend` | `8443` | `8000` | http://localhost:8443 (`/docs`) | REST API (`/api/v1/*`) |
| PostgreSQL | `postgres` | `5432` | `5432` | localhost:5432 | Primary database |
| pgAdmin (dev profile) | `pgadmin` | `5050` | `80` | http://localhost:5050 | Database admin UI |

Notes:
- Frontend to backend flow: browser hits `1337`, and Nginx forwards API calls to backend `8443`.
- `pgAdmin` only runs when dev profile is enabled: `docker compose --profile dev up`.
- Local frontend development uses Vite on `5173` (`npm run dev`), not Docker port `1337`.

## Data Sources (free, no API key required)

| Category       | Sources |
|----------------|---------|
| Security News  | 79 RSS feeds — Hacker News, Dark Reading, Bleeping Computer, Krebs, CyberScoop, Mandiant, Trend Micro, Proofpoint, Elastic, CISA, NSA, FBI, Europol, + many more |
| Google News    | 20 cybersecurity topic queries via Google News RSS (ransomware, zero-day, APT, supply chain, etc.) |
| CVE / Threats  | NVD REST API v2 (48h rolling window) |
| Geo News       | GDELT 2.0 DOC API (20 queries, 50 articles each, 72h window) |
| Financial      | yFinance (18 tickers: PANW, CRWD, FTNT, NVDA, MSFT, GOOGL, ...) |
| Certifications | 13 feeds — NIST, ENISA, CISA, OWASP, FIRST, ISC2, ISACA, NCSC UK/NL, CERT-FR, JPCERT, ACSC, CERT-IN, KrCERT |
| AI / Tech News | TechCrunch AI, VentureBeat, MIT Tech Review, Wired, BBC Technology, The Verge, Ars Technica |

## Optional API Keys (adds more data)

Add to `backend/.env`:

```env
YOUTUBE_API_KEY=<your-key>   # Enables live stream discovery
```

## API Endpoints

```
GET /api/v1/intelligence/        Paginated news feed
GET /api/v1/intelligence/top     Top-N by impact score
GET /api/v1/intelligence/map     Geo-tagged events for Leaflet
GET /api/v1/intelligence/stats   Totals by type & country
GET /api/v1/threats/             CVE list with filters
GET /api/v1/threats/critical     Critical + High CVEs
GET /api/v1/financial/           Latest stock snapshots
GET /api/v1/financial/movers     Top gainers & losers
GET /api/v1/streams/             Live YouTube streams
GET /api/v1/certifications/      Standards body updates
GET /health                      Health check
```

## Project Structure

```
cyberverse/
├── backend/
│   ├── app/
│   │   ├── collectors/      RSS (79), Google News (20), GDELT (20), CVE, Financial, YouTube, Cert (13)
│   │   ├── models/          SQLAlchemy ORM models
│   │   ├── schemas/         Pydantic v2 schemas
│   │   ├── routers/         FastAPI route handlers
│   │   ├── config.py        Settings (pydantic-settings)
│   │   ├── database.py      Async engine + session
│   │   ├── scheduler.py     APScheduler jobs
│   │   ├── normalizer.py    Upsert helpers
│   │   ├── sentiment.py     VADER sentiment + impact scoring
│   │   └── main.py          FastAPI app
│   ├── alembic/             DB migrations
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── views/           7 page views
    │   ├── components/      UI, layout, charts, map
    │   ├── stores/          Pinia state (intelligence, financial, threats, streams)
    │   ├── services/api.ts  Axios API wrappers
    │   └── types/index.ts   TypeScript interfaces
    ├── package.json
    └── Dockerfile
```

## Scheduler Intervals

| Collector | Interval |
|-----------|----------|
| RSS + Google News + GDELT + Certs | Every 15 min |
| CVE (NVD) | Every 30 min |
| Financial (yFinance) | Every 60 min |

---

To setup follow the instructions.
