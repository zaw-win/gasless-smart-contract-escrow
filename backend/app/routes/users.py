from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.wallet import create_user_and_wallet_if_not_exists

router = APIRouter(prefix="/user")

class UserInfo(BaseModel):
    email: str

@router.post("/status")
def check_or_create_user(data: UserInfo):
    try:
        create_user_and_wallet_if_not_exists(data.email)
    except Exception as e:
        raise HTTPException(500, f"Error checking/creating user: {str(e)}") 