from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pwdlib import PasswordHash
from app.core.config import settings

password_hash=PasswordHash.recommended()
def verify_password(plain: str, hashed: str) -> bool: return password_hash.verify(plain, hashed)
def hash_password(password: str) -> str: return password_hash.hash(password)
def create_access_token(subject: str, role: str) -> str:
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub":subject,"role":role,"exp":expire},settings.jwt_secret,algorithm=settings.jwt_algorithm)
def decode_token(token: str):
    try: return jwt.decode(token,settings.jwt_secret,algorithms=[settings.jwt_algorithm])
    except JWTError: return None
