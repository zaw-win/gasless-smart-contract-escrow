
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SERVER_SECRET").encode()
fernet = Fernet(SECRET)

def encrypt_key(raw: bytes) -> str:
    return fernet.encrypt(raw).decode()

def decrypt_key(token: str) -> bytes:
    return fernet.decrypt(token.encode())

