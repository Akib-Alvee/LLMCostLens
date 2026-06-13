from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
ApiKeyHeader = Annotated[str | None, Header(alias="x-api-key")]


async def require_api_user(
    db: DatabaseSession,
    x_api_key: ApiKeyHeader = None,
) -> User:
    if not x_api_key:
        raise _unauthorized()

    user = await UserRepository(db).get_active_user_by_api_key(x_api_key)
    if user is None:
        raise _unauthorized()

    return user


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API key",
    )
