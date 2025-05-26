import asyncio
from infraestructure.db.config import Base, engine  # tu AsyncEngine
from infraestructure.db.models import MessageModel, MessageTagModel, TagsModel

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
