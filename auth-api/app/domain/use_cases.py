from typing import Dict, List, Optional

from sqlalchemy import UUID

from app.security.password import verify_password
from app.security.token import create_access_token
from app.api.schemas import UserCreate, UserCredentials, UserSearch
from app.data.db.repository import UserRepository

async def register_user(user_repo: UserRepository, user_data: UserCreate) -> UserSearch:
    
    new_user = await user_repo.create_user(user_data)

    if not new_user:
        return None

    return UserSearch(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username
    )


async def login_user(user_repo: UserRepository, user_data: UserCredentials) -> Dict[str, str]:

    user = await user_repo.get_user_by_email(user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password) or not user.is_active:
        return None

    token = create_access_token({"sub": str(user.id), "email": str(user.email)})
        
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
        }
async def get_user_by_id(repo: UserRepository, user_id: UUID) -> UserSearch:
    user = await repo.get_user_by_id(user_id=user_id)
    return(UserSearch(id=user.id, email=user.email, username=user.username))

async def search_users(
    email: Optional[str],
    user_repo: UserRepository
) -> list[UserSearch]:
    
    users = await user_repo.search_users_by_email(email)
    
    return [
        UserSearch(
            id=user.id,
            email=user.email,
            username=user.username,
        ) for user in users
    ]

async def search_users_list(repo : UserRepository, user_ids:List[UUID]):
    users = await repo.search_users_by_ids(user_ids)

    return [
        UserSearch(
            id=user.id,
            email=user.email,
            username=user.username,
        ) for user in users
    ]