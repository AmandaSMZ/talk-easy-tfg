import asyncio
from app.data.db.db import engine
from app.data.db.base import Base
from app.data.db import models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
