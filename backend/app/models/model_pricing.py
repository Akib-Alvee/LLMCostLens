from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, utc_now


class ModelPricing(Base):
    __tablename__ = "model_pricing"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    model_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )
    input_cost_per_1k_tokens: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    output_cost_per_1k_tokens: Mapped[Decimal] = mapped_column(Numeric(18, 10))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
