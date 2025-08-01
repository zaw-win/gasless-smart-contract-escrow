from fastapi import HTTPException, Request, Depends
from jose import jwt, JWTError
from eth_account import Account
from .crypto import encrypt_key, decrypt_key
from ..database.utils import get_db_conn
import os
from dotenv import load_dotenv
from ..database.users import upsert_users

load_dotenv()
SECRET = os.getenv("NEXTAUTH_SECRET")
ALGORITHM = "HS256"

async def authenticate_user(req:Request):
    # NextAuth sets session in this cookie
    token = req.cookies.get("next-auth.session-token")
    if not token:
        raise HTTPException(401, "Not Authenticated.")
    
    try:
        payload = jwt.decode(token,SECRET, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(401, "Invalid Token Payload - No email found")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.JWTError as e:
        raise HTTPException(401, f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(401, f"Token validation error: {str(e)}")
