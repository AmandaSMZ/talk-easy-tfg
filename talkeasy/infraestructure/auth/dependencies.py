from uuid import UUID
from fastapi import Header, HTTPException
from passlib.context import CryptContext

INTERNAL_SECRET = "bcrypt$$2b$12$BWzluYdeH7wC6TPzkzHILeIb.b86ccX88tOzCdlsgNx8LPuVCehcK"

MESSAGE_FORBIDDEN = "Access forbidden: Invalid internal token"


pwd_context = CryptContext(
    schemes=["django_bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(
    x_user_id: UUID = Header(...),
    x_username: str = Header(default=None)):
    return {"id": x_user_id, "username": x_username}


def verify_internal_token_only(x_internal_token: str = Header(...)):
    
    if not verify_password(x_internal_token, INTERNAL_SECRET):
        raise HTTPException(status_code=403, detail=MESSAGE_FORBIDDEN)
    
def verify_ws_token(token):
    return verify_password(token, INTERNAL_SECRET)
    