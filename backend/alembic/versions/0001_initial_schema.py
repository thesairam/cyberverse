"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "intelligence_events",
        sa.Column("id",                sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("external_id",       sa.String(512)),
        sa.Column("source_url",        sa.Text, nullable=False, unique=True),
        sa.Column("title",             sa.Text, nullable=False),
        sa.Column("summary",           sa.Text),
        sa.Column("content",           sa.Text),
        sa.Column("event_type",        sa.String(32), nullable=False),
        sa.Column("category_tags",     postgresql.ARRAY(sa.Text)),
        sa.Column("entities_mentioned",postgresql.ARRAY(sa.Text)),
        sa.Column("source_name",       sa.String(256), nullable=False),
        sa.Column("relevant_body",     sa.String(256)),
        sa.Column("author",            sa.String(256)),
        sa.Column("country",           sa.String(128)),
        sa.Column("city",              sa.String(128)),
        sa.Column("latitude",          sa.Float),
        sa.Column("longitude",         sa.Float),
        sa.Column("sentiment_score",   sa.Float),
        sa.Column("impact_score",      sa.Float),
        sa.Column("importance_rank",   sa.Integer),
        sa.Column("published_at",      sa.DateTime(timezone=True)),
        sa.Column("collected_at",      sa.DateTime(timezone=True)),
        sa.Column("created_at",        sa.DateTime(timezone=True)),
        sa.Column("updated_at",        sa.DateTime(timezone=True)),
        sa.Column("extra",             postgresql.JSONB),
    )
    op.create_index("ix_intel_event_type",   "intelligence_events", ["event_type"])
    op.create_index("ix_intel_published_at", "intelligence_events", ["published_at"])
    op.create_index("ix_intel_impact_score", "intelligence_events", ["impact_score"])
    op.create_index("ix_intel_country",      "intelligence_events", ["country"])

    op.create_table(
        "financial_snapshots",
        sa.Column("id",          sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("ticker",      sa.String(16), nullable=False),
        sa.Column("company_name",sa.String(256), nullable=False),
        sa.Column("sector",      sa.String(64)),
        sa.Column("price",       sa.Float),
        sa.Column("open_price",  sa.Float),
        sa.Column("high",        sa.Float),
        sa.Column("low",         sa.Float),
        sa.Column("volume",      sa.BigInteger),
        sa.Column("market_cap",  sa.Float),
        sa.Column("pe_ratio",    sa.Float),
        sa.Column("change_pct",  sa.Float),
        sa.Column("currency",    sa.String(8)),
        sa.Column("exchange",    sa.String(32)),
        sa.Column("snapshot_at", sa.DateTime(timezone=True)),
        sa.Column("created_at",  sa.DateTime(timezone=True)),
    )
    op.create_index("ix_fin_ticker",      "financial_snapshots", ["ticker"])
    op.create_index("ix_fin_snapshot_at", "financial_snapshots", ["snapshot_at"])

    op.create_table(
        "live_streams",
        sa.Column("id",            sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("video_id",      sa.String(128), nullable=False, unique=True),
        sa.Column("title",         sa.Text, nullable=False),
        sa.Column("channel_name",  sa.String(256)),
        sa.Column("channel_id",    sa.String(128)),
        sa.Column("stream_url",    sa.Text, nullable=False),
        sa.Column("thumbnail_url", sa.Text),
        sa.Column("is_live",       sa.Boolean),
        sa.Column("viewer_count",  sa.Integer),
        sa.Column("category_tags", postgresql.ARRAY(sa.Text)),
        sa.Column("started_at",    sa.DateTime(timezone=True)),
        sa.Column("ended_at",      sa.DateTime(timezone=True)),
        sa.Column("collected_at",  sa.DateTime(timezone=True)),
        sa.Column("created_at",    sa.DateTime(timezone=True)),
    )

    op.create_table(
        "threat_indicators",
        sa.Column("id",               sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("indicator_id",     sa.String(64), nullable=False, unique=True),
        sa.Column("title",            sa.Text, nullable=False),
        sa.Column("description",      sa.Text),
        sa.Column("indicator_type",   sa.String(32), nullable=False),
        sa.Column("severity",         sa.String(16)),
        sa.Column("cvss_score",       sa.Float),
        sa.Column("cvss_vector",      sa.String(256)),
        sa.Column("affected_products",postgresql.ARRAY(sa.Text)),
        sa.Column("references",       postgresql.ARRAY(sa.Text)),
        sa.Column("cwe_ids",          postgresql.ARRAY(sa.Text)),
        sa.Column("tags",             postgresql.ARRAY(sa.Text)),
        sa.Column("source_name",      sa.String(128)),
        sa.Column("published_at",     sa.DateTime(timezone=True)),
        sa.Column("modified_at",      sa.DateTime(timezone=True)),
        sa.Column("collected_at",     sa.DateTime(timezone=True)),
        sa.Column("created_at",       sa.DateTime(timezone=True)),
        sa.Column("updated_at",       sa.DateTime(timezone=True)),
        sa.Column("extra",            postgresql.JSONB),
    )
    op.create_index("ix_threat_severity",   "threat_indicators", ["severity"])
    op.create_index("ix_threat_cvss",       "threat_indicators", ["cvss_score"])

    op.create_table(
        "certification_updates",
        sa.Column("id",          sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("body_name",   sa.String(128), nullable=False),
        sa.Column("standard_id", sa.String(128)),
        sa.Column("title",       sa.Text, nullable=False),
        sa.Column("summary",     sa.Text),
        sa.Column("update_type", sa.String(32)),
        sa.Column("source_url",  sa.Text),
        sa.Column("region",      sa.String(128)),
        sa.Column("published_at",sa.DateTime(timezone=True)),
        sa.Column("collected_at",sa.DateTime(timezone=True)),
        sa.Column("created_at",  sa.DateTime(timezone=True)),
        sa.Column("extra",       postgresql.JSONB),
    )


def downgrade() -> None:
    op.drop_table("certification_updates")
    op.drop_table("threat_indicators")
    op.drop_table("live_streams")
    op.drop_table("financial_snapshots")
    op.drop_table("intelligence_events")
