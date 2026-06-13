from datetime import datetime
from decimal import Decimal
from typing import Any

from app.schemas.base import CamelCaseModel


class OverviewDto(CamelCaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_tokens: int
    estimated_cost_usd: Decimal
    average_latency_ms: float


class RequestLogDto(CamelCaseModel):
    trace_id: str
    user_id: str
    endpoint_name: str
    model_name: str
    prompt_preview: str
    response_preview: str | None = None
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: Decimal
    latency_ms: int
    status: str
    error_code: str | None = None
    error_message: str | None = None
    metadata_json: dict[str, Any] | None = None
    created_at: datetime


class TimeSeriesPointDto(CamelCaseModel):
    timestamp: datetime
    request_count: int
    total_tokens: int
    estimated_cost_usd: Decimal
    average_latency_ms: float


class BreakdownPointDto(CamelCaseModel):
    name: str
    request_count: int
    total_tokens: int
    estimated_cost_usd: Decimal
