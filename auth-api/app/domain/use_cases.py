from typing import Dict

from app.security.password import verify_password
from app.security.token import create_access_token
from app.api.schemas import UserCredentials, UserRead
from app.data.db.repository import UserRepository

async def register_user(user_repo: UserRepository, user_data: UserCredentials) -> UserRead:
    
    new_user = await user_repo.create_user(user_data)

    if not new_user:
        return None

    return UserRead(
        id=new_user.id,
        email=new_user.email,
        created_at=new_user.created_at
    )


async def login_user(user_repo: UserRepository, user_data: UserCredentials) -> Dict[str, str]:

    user = await user_repo.get_user_by_email(user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        return None

    token = create_access_token({"sub": str(user.id)})
        
    return {
        "access_token": token,
        "token_type": "bearer"
        }

async def search_users(
    email: str,
    user_repo: UserRepository
) -> list[UserRead]:
    
    users = await user_repo.search_users_by_email(email)
    
    return [
        UserRead(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        ) for user in users
    ]