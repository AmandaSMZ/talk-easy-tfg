from fastapi import Depends, Header
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.token import decode_access_token
from app.data.db.models import User
from typing import Optional
from app.dependencies.repository import get_user_repository
from app.data.db.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="User ID header missing")
    return x_user_id