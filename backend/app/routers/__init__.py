from fastapi import APIRouter
from app.routers import intelligence, financial, threats, streams, certifications
api_router = APIRouter()
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["Intelligence"])
api_router.include_router(financial.router,    prefix="/financial",   tags=["Financial"])
api_router.include_router(threats.router,      prefix="/threats",     tags=["Threats"])
api_router.include_router(streams.router,      prefix="/streams",     tags=["Streams"])
api_router.include_router(certifications.router, prefix="/certifications", tags=["Certifications"])
