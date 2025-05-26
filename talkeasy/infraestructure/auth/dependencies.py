from uuid import UUID
from fastapi import Header, HTTPException

INTERNAL_SECRET = "tu_token_super_secreto"
MESSAGE_FORBIDDEN = "Access forbidden: Invalid internal token"

def get_current_user(
        
    x_user_id: UUID = Header(...),
    x_username: str = Header(default=None)):

    return {"id": x_user_id, "username": x_username}


def verify_internal_token_only(x_internal_token: str = Header(...)):
    
    if x_internal_token != INTERNAL_SECRET:
        raise HTTPException(status_code=403, detail=MESSAGE_FORBIDDEN)
    
def verify_ws_token(token):
    return token != INTERNAL_SECRET
    