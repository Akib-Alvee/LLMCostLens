from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_active_user_by_api_key(self, api_key: str) -> User | None:
        statement = select(User).where(
            User.api_key_hash == hash_api_key(api_key),
            User.is_active.is_(True),
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
