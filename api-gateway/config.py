
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    AUTH_API_URL:str
    TALKEASY_API_URL:str
    TAGGING_API_URL:str

    JWT_ALGORITHM: str = "RS256"
    PUBLIC_KEY_PATH: str = "public_key.pem"

    @property
    def JWT_SECRET_KEY(self) -> bytes:
        return Path(self.PUBLIC_KEY_PATH).read_bytes()
    

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
