from infraestructure.db.config import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
