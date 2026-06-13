from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class AiRequestLog(Base):
    __tablename__ = "ai_request_logs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    trace_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )
    endpoint_name: Mapped[str] = mapped_column(String(255), index=True)
    model_name: Mapped[str] = mapped_column(String(255), index=True)
    prompt_preview: Mapped[str] = mapped_column(Text)
    response_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_hash: Mapped[str] = mapped_column(String(255), index=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer)
    completion_tokens: Mapped[int] = mapped_column(Integer)
    total_tokens: Mapped[int] = mapped_column(Integer)
    estimated_cost_usd: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    latency_ms: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), index=True)
    error_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        index=True,
    )
