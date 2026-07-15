import asyncio

from app.db.session import AsyncSessionLocal
from app.repositories.user import UserRepository


async def main():
    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)

        users = await repo.get_all()

        print(users)


asyncio.run(main())