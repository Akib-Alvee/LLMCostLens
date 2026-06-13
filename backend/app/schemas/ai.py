from decimal import Decimal
from typing import Any

from app.schemas.base import CamelCaseModel


class SummarizeRequest(CamelCaseModel):
    text: str
    model_name: str = "local-mock"
    summary_style: str = "concise"


class ExplainCodeRequest(CamelCaseModel):
    code: str
    language: str = "unknown"
    model_name: str = "local-mock"


class ExtractJsonRequest(CamelCaseModel):
    text: str
    schema_name: str = "generic"
    model_name: str = "local-mock"


class UsageDto(CamelCaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: Decimal
    latency_ms: int


class ErrorDto(CamelCaseModel):
    code: str
    message: str


class AiResponseDto(CamelCaseModel):
    success: bool
    trace_id: str
    result: Any | None = None
    error: ErrorDto | None = None
    usage: UsageDto | None = None
