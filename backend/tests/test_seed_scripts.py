from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import app.models  # noqa: F401
from app.core.security import hash_api_key
from app.db.base import Base
from app.models.model_pricing import ModelPricing
from app.models.user import User
from scripts.seed_model_pricing import seed_model_pricing
from scripts.seed_users import seed_users


@pytest.mark.asyncio
async def test_seed_scripts_are_idempotent() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory.begin() as session:
        assert await seed_users(session) == 2
        assert await seed_model_pricing(session) == 3

    async with session_factory.begin() as session:
        assert await seed_users(session) == 0
        assert await seed_model_pricing(session) == 0

    async with session_factory() as session:
        users = (await session.execute(select(User))).scalars().all()
        pricing = (await session.execute(select(ModelPricing))).scalars().all()

    assert {user.name for user in users} == {"Demo User 1", "Demo User 2"}
    assert {user.api_key_hash for user in users} == {
        hash_api_key("demo-user-1-key"),
        hash_api_key("demo-user-2-key"),
    }
    assert all("demo-user" not in user.api_key_hash for user in users)
    assert {
        row.model_name: (
            row.input_cost_per_1k_tokens,
            row.output_cost_per_1k_tokens,
        )
        for row in pricing
    } == {
        "local-mock": (Decimal("0"), Decimal("0")),
        "gpt-4o-mini": (Decimal("0.0001500000"), Decimal("0.0006000000")),
        "gpt-4o": (Decimal("0.0050000000"), Decimal("0.0150000000")),
    }

    await engine.dispose()
