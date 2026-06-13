from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace

from app.schemas import (
    AiResponseDto,
    ExplainCodeRequest,
    ExtractJsonRequest,
    RequestLogDto,
    SummarizeRequest,
    UsageDto,
)


def test_ai_request_defaults_and_camel_case_input() -> None:
    summarize = SummarizeRequest.model_validate({"text": "Hello"})
    explain = ExplainCodeRequest.model_validate(
        {
            "code": "print('hello')",
            "modelName": "gpt-4o-mini",
        }
    )
    extract = ExtractJsonRequest.model_validate({"text": "Name: Ada"})

    assert summarize.model_dump() == {
        "text": "Hello",
        "modelName": "local-mock",
        "summaryStyle": "concise",
    }
    assert explain.model_name == "gpt-4o-mini"
    assert explain.language == "unknown"
    assert extract.schema_name == "generic"
    assert extract.model_name == "local-mock"


def test_ai_response_serializes_nested_fields_as_camel_case() -> None:
    response = AiResponseDto(
        success=True,
        trace_id="trace-1",
        result={"summary": "Hello"},
        usage=UsageDto(
            prompt_tokens=10,
            completion_tokens=4,
            total_tokens=14,
            estimated_cost_usd=Decimal("0.0015"),
            latency_ms=25,
        ),
    )

    assert response.model_dump(mode="json") == {
        "success": True,
        "traceId": "trace-1",
        "result": {"summary": "Hello"},
        "error": None,
        "usage": {
            "promptTokens": 10,
            "completionTokens": 4,
            "totalTokens": 14,
            "estimatedCostUsd": "0.0015",
            "latencyMs": 25,
        },
    }


def test_request_log_dto_validates_from_model_attributes() -> None:
    created_at = datetime(2026, 6, 13, tzinfo=timezone.utc)
    request_log = SimpleNamespace(
        trace_id="trace-1",
        user_id="user-1",
        endpoint_name="summarize",
        model_name="local-mock",
        prompt_preview="Hello",
        response_preview="Summary",
        prompt_tokens=10,
        completion_tokens=4,
        total_tokens=14,
        estimated_cost_usd=Decimal("0"),
        latency_ms=12,
        status="success",
        error_code=None,
        error_message=None,
        metadata_json={"source": "test"},
        created_at=created_at,
    )

    dto = RequestLogDto.model_validate(request_log)

    assert dto.model_dump()["traceId"] == "trace-1"
    assert dto.model_dump()["metadataJson"] == {"source": "test"}
    assert dto.model_dump()["createdAt"] == created_at
