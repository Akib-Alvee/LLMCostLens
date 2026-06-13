import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key
from app.db.session import AsyncSessionFactory, engine
from app.models.user import User

DEMO_USERS = (
    ("Demo User 1", "demo-user-1-key"),
    ("Demo User 2", "demo-user-2-key"),
)


async def seed_users(session: AsyncSession) -> int:
    api_key_hashes = [hash_api_key(api_key) for _, api_key in DEMO_USERS]
    result = await session.execute(
        select(User.api_key_hash).where(User.api_key_hash.in_(api_key_hashes))
    )
    existing_hashes = set(result.scalars())

    users = [
        User(name=name, api_key_hash=api_key_hash)
        for (name, _), api_key_hash in zip(
            DEMO_USERS,
            api_key_hashes,
            strict=True,
        )
        if api_key_hash not in existing_hashes
    ]
    session.add_all(users)
    return len(users)


async def main() -> None:
    async with AsyncSessionFactory.begin() as session:
        created_count = await seed_users(session)

    await engine.dispose()
    print(f"Created {created_count} demo user(s).")


if __name__ == "__main__":
    asyncio.run(main())
