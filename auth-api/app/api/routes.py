from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordBearer
from app.api.schemas import UserCredentials, Token, UserCreate, UserSearch, UsersIdRequest
from app.domain.use_cases import get_user_by_id, register_user, login_user, search_users, search_users_list
from app.data.db.repository import UserRepository
from app.dependencies.repository import get_user_repository
from app.data.db.models import User
from app.dependencies.auth import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register",status_code=status.HTTP_201_CREATED, response_model=UserSearch)
async def register(
    user: UserCreate, 
    user_repo: UserRepository = Depends(get_user_repository)
    ):
    new_user = await register_user(user_repo, user)

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )
    return new_user

@router.post("/login", response_model=Token)
async def login(
    user: UserCredentials, 
    user_repo: UserRepository = Depends(get_user_repository)
    ):
    token = await login_user(user_repo,user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return token

@router.get("/me", response_model=UserSearch)
async def get_me(user_id: User = Depends(get_current_user),
                 repo: UserRepository = Depends(get_user_repository)):

    return await get_user_by_id(repo, user_id)
    

@router.get("/search/", status_code=status.HTTP_200_OK, response_model=List[UserSearch])
async def search_users_route(
    email: Optional[str] = Query(None),
    _: User = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository)
):
    result = await search_users(email, user_repo)
    
    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return result

@router.get("/search/user-id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSearch)
async def search_users_route(
    user_id: str,
    _: User = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository)
):
    result = await get_user_by_id(user_id=user_id, repo=user_repo)
    
    if not result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return result

@router.post("/search/users", status_code=status.HTTP_200_OK, response_model=List[UserSearch])
async def search_users_route(
    request: UsersIdRequest,
    _: User = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repository)
):
    result = await search_users_list(user_repo,request.users_id)
    return result or []
