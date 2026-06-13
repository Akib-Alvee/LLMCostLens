import app.models  # noqa: F401
from app.db.base import Base


def test_model_metadata_contains_expected_tables() -> None:
    assert set(Base.metadata.tables) == {
        "ai_request_logs",
        "model_pricing",
        "users",
    }


def test_request_log_user_foreign_key() -> None:
    user_id = Base.metadata.tables["ai_request_logs"].c.user_id

    assert {foreign_key.target_fullname for foreign_key in user_id.foreign_keys} == {
        "users.id"
    }
