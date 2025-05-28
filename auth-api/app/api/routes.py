from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.schemas import UserRead,UserCredentials, Token
from app.domain.use_cases import register_user, login_user, search_users
from app.data.db.repository import UserRepository
from app.dependencies.repository import get_user_repository
from app.data.db.models import User
from app.dependencies.auth import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register",status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register(
    user: UserCredentials, 
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

@router.get("/me", response_model=UserRead)
async def get_me(user_id: User = Depends(get_current_user),
                 repo: UserRepository = Depends(get_user_repository)):

    user = await repo.get_user_by_id(user_id)
    return(UserRead(id=user.id, email=user.email, created_at=user.created_at))

@router.get("/users/search/{email}", response_model=list[UserRead])
async def search_users_route(
    email: str,
    _: User = Depends(get_current_user),  # solo verifico que el usuario está autenticado, aunque no lo uso
    user_repo: UserRepository = Depends(get_user_repository)
):
    return await search_users(email, user_repo)
