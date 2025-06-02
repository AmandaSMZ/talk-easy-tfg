from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserCredentials):
    username: str

class UserSearch(BaseModel):
    id:UUID
    email: EmailStr
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id:UUID
    username: str

class UsersIdRequest(BaseModel):
    users_id: List[UUID]
