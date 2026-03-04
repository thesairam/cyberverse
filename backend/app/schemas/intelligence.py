from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field


class EventType(str, Enum):
    NEWS = "NEWS"; POLICY = "POLICY"; PRODUCT = "PRODUCT"; FINANCIAL = "FINANCIAL"
    VIDEO = "VIDEO"; CERTIFICATION = "CERTIFICATION"; STARTUP = "STARTUP"; ALERT = "ALERT"

class ThreatSeverity(str, Enum):
    CRITICAL = "CRITICAL"; HIGH = "HIGH"; MEDIUM = "MEDIUM"; LOW = "LOW"; INFO = "INFO"

class ThreatType(str, Enum):
    CVE = "CVE"; ZERO_DAY = "ZERO-DAY"; MALWARE = "MALWARE"; IOC = "IOC"; ADVISORY = "ADVISORY"


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class IntelligenceEventCreate(_Base):
    title: str; summary: Optional[str] = None; content: Optional[str] = None
    event_type: EventType; source_url: str; source_name: str
    category_tags: list[str] = Field(default_factory=list)
    entities_mentioned: list[str] = Field(default_factory=list)
    relevant_body: Optional[str] = None; author: Optional[str] = None
    country: Optional[str] = None; city: Optional[str] = None
    latitude: Optional[float] = None; longitude: Optional[float] = None
    sentiment_score: Optional[float] = 0.0; impact_score: Optional[float] = 0.0
    published_at: Optional[datetime] = None; extra: dict[str, Any] = Field(default_factory=dict)


class IntelligenceEventOut(_Base):
    id: uuid.UUID; title: str; summary: Optional[str] = None
    event_type: str; source_name: str; source_url: str
    category_tags: list[str] = []; entities_mentioned: list[str] = []
    relevant_body: Optional[str] = None; country: Optional[str] = None
    city: Optional[str] = None; latitude: Optional[float] = None
    longitude: Optional[float] = None; sentiment_score: float = 0.0
    impact_score: float = 0.0; published_at: Optional[datetime] = None
    collected_at: Optional[datetime] = None; extra: dict[str, Any] = {}


class FinancialSnapshotOut(_Base):
    id: uuid.UUID; ticker: str; company_name: str; sector: Optional[str] = None
    price: Optional[float] = None; open_price: Optional[float] = None
    high: Optional[float] = None; low: Optional[float] = None
    volume: Optional[int] = None; market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None; change_pct: Optional[float] = None
    currency: str = "USD"; exchange: Optional[str] = None; snapshot_at: Optional[datetime] = None


class LiveStreamOut(_Base):
    id: uuid.UUID; video_id: str; title: str; channel_name: Optional[str] = None
    stream_url: str; thumbnail_url: Optional[str] = None; is_live: bool = False
    viewer_count: int = 0; category_tags: list[str] = []
    started_at: Optional[datetime] = None; collected_at: Optional[datetime] = None


class ThreatIndicatorOut(_Base):
    id: uuid.UUID; indicator_id: str; title: str; description: Optional[str] = None
    indicator_type: str; severity: Optional[str] = None; cvss_score: Optional[float] = None
    cvss_vector: Optional[str] = None; affected_products: list[str] = []
    references: list[str] = []; cwe_ids: list[str] = []; tags: list[str] = []
    source_name: Optional[str] = None; published_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None


class CertificationUpdateOut(_Base):
    id: uuid.UUID; body_name: str; standard_id: Optional[str] = None
    title: str; summary: Optional[str] = None; update_type: Optional[str] = None
    source_url: Optional[str] = None; region: Optional[str] = None
    published_at: Optional[datetime] = None


T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int; page: int; page_size: int; pages: int; items: list[T]


class QueryFilters(BaseModel):
    event_type: Optional[EventType] = None; category: Optional[str] = None
    country: Optional[str] = None; source_name: Optional[str] = None
    from_date: Optional[datetime] = None; to_date: Optional[datetime] = None
    min_impact: Optional[float] = None; search: Optional[str] = None
    page: int = Field(1, ge=1); page_size: int = Field(20, ge=1, le=100)
