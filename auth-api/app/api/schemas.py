from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
