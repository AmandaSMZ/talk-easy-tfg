
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    JWT_ALGORITHM: str = "RS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PRIVATE_KEY_PATH: str = "private_key.pem"

    @property
    def DATABASE_URL(self) -> str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    @property
    def JWT_SECRET_KEY(self) -> bytes:
        return Path(self.PRIVATE_KEY_PATH).read_bytes()

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()