import asyncio

from travel_ai_backend.app.db.init_db import init_db
from travel_ai_backend.app.db.session import SessionLocal


async def create_init_data() -> None:
    async with SessionLocal() as session:
        await init_db(session)


async def main() -> None:
    await create_init_data()


if __name__ == "__main__":
    asyncio.run(main())
