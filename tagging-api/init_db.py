import asyncio
from app.infraestructure.db.db import engine
from app.infraestructure.db.base import Base
from app.infraestructure.db.models import TagModel

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
