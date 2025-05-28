import asyncio
from infraestructure.db.config import engine
from infraestructure.db.base import Base
from infraestructure.db.models import MessageModel, MessageTagUserModel, Conversation

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())