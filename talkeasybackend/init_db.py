import asyncio
from infraestructure.postgres.models.user_model import User
from infraestructure.postgres.models.message_model import Message
from infraestructure.postgres.database import Base
from infraestructure.postgres.database import engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas creadas (si no existían)")

if __name__ == "__main__":
    asyncio.run(create_tables())
