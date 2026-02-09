import asyncio

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.auth.passwords import hash_password


async def main():
    async with AsyncSessionLocal() as session:
        user = User(
            email="test@example.com",
            hashed_password=hash_password("test123"),
            is_active=True,
            is_admin=False,
        )
        session.add(user)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
