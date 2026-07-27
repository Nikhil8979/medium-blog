from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import get_app_config

config = get_app_config()
password_hash = PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password)->bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt

