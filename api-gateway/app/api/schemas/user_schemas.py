from typing import List
from pydantic import BaseModel, EmailStr

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserCredentials):
    username: str

class UserSearch(BaseModel):
    id: str
    email: EmailStr
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id:str
    username: str

class UsersIdRequest(BaseModel):
    users_id: List[str]