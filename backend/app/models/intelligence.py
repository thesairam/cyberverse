import uuid
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class IntelligenceEvent(Base):
    __tablename__ = "intelligence_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(512), nullable=True)
    source_url = Column(Text, nullable=False, unique=True)
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    event_type = Column(String(32), nullable=False)
    category_tags = Column(ARRAY(Text), default=list)
    entities_mentioned = Column(ARRAY(Text), default=list)
    source_name = Column(String(256), nullable=False)
    relevant_body = Column(String(256), nullable=True)
    author = Column(String(256), nullable=True)
    country = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sentiment_score = Column(Float, default=0.0)
    impact_score = Column(Float, default=0.0)
    importance_rank = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=_now)
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)
    extra = Column(JSONB, default=dict)
    __table_args__ = (UniqueConstraint("source_url", name="uq_intel_source_url"),)


class FinancialSnapshot(Base):
    __tablename__ = "financial_snapshots"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(16), nullable=False)
    company_name = Column(String(256), nullable=False)
    sector = Column(String(64), nullable=True)
    price = Column(Float, nullable=True)
    open_price = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    volume = Column(BigInteger, nullable=True)
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    change_pct = Column(Float, nullable=True)
    currency = Column(String(8), default="USD")
    exchange = Column(String(32), nullable=True)
    snapshot_at = Column(DateTime(timezone=True), default=_now)
    created_at = Column(DateTime(timezone=True), default=_now)


class LiveStream(Base):
    __tablename__ = "live_streams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(String(128), nullable=False, unique=True)
    title = Column(Text, nullable=False)
    channel_name = Column(String(256), nullable=True)
    channel_id = Column(String(128), nullable=True)
    stream_url = Column(Text, nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    is_live = Column(Boolean, default=False)
    viewer_count = Column(Integer, default=0)
    category_tags = Column(ARRAY(Text), default=list)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=_now)
    created_at = Column(DateTime(timezone=True), default=_now)


class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    indicator_id = Column(String(64), nullable=False, unique=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    indicator_type = Column(String(32), nullable=False)
    severity = Column(String(16), nullable=True)
    cvss_score = Column(Float, nullable=True)
    cvss_vector = Column(String(256), nullable=True)
    affected_products = Column(ARRAY(Text), default=list)
    references = Column(ARRAY(Text), default=list)
    cwe_ids = Column(ARRAY(Text), default=list)
    tags = Column(ARRAY(Text), default=list)
    source_name = Column(String(128), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    modified_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=_now)
    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)
    extra = Column(JSONB, default=dict)


class CertificationUpdate(Base):
    __tablename__ = "certification_updates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body_name = Column(String(128), nullable=False)
    standard_id = Column(String(128), nullable=True)
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    update_type = Column(String(32), nullable=True)
    source_url = Column(Text, nullable=True)
    region = Column(String(128), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=_now)
    created_at = Column(DateTime(timezone=True), default=_now)
    extra = Column(JSONB, default=dict)
