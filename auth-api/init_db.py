import asyncio
from app.db import Base, engine 
import app.models 

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
