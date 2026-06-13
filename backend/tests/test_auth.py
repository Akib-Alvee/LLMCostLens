from collections.abc import AsyncGenerator
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import app.models  # noqa: F401
from app.api.dependencies import require_api_user
from app.core.security import hash_api_key
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_require_api_user_authenticates_only_active_users() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_factory.begin() as session:
        session.add_all(
            [
                User(
                    name="Active User",
                    api_key_hash=hash_api_key("active-key"),
                ),
                User(
                    name="Inactive User",
                    api_key_hash=hash_api_key("inactive-key"),
                    is_active=False,
                ),
            ]
        )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    test_app = FastAPI()
    test_app.dependency_overrides[get_db] = override_get_db

    @test_app.get("/protected")
    async def protected(
        user: Annotated[User, Depends(require_api_user)],
    ) -> dict[str, str]:
        return {"name": user.name}

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        missing_response = await client.get("/protected")
        invalid_response = await client.get(
            "/protected",
            headers={"x-api-key": "invalid-key"},
        )
        inactive_response = await client.get(
            "/protected",
            headers={"x-api-key": "inactive-key"},
        )
        valid_response = await client.get(
            "/protected",
            headers={"x-api-key": "active-key"},
        )

    assert missing_response.status_code == 401
    assert invalid_response.status_code == 401
    assert inactive_response.status_code == 401
    assert valid_response.status_code == 200
    assert valid_response.json() == {"name": "Active User"}

    async with session_factory() as session:
        repository = UserRepository(session)
        assert await repository.get_active_user_by_api_key("active-key") is not None
        assert await repository.get_active_user_by_api_key("inactive-key") is None

    await engine.dispose()
