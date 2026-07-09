import jwt
from pwdlib import PasswordHash
from fastapi import HTTPException
from jwt import ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv


pwd_hasher = PasswordHash.recommended()

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def hashed(raw_pwd):
    return pwd_hasher.hash(raw_pwd)



def pwd_verify(raw_pwd, hashed_pwd):
    return pwd_hasher.verify(raw_pwd, hashed_pwd)



def create_token(user_id):
    payload = {"id": user_id}
    payload.update(exp=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    encode_jwt = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return encode_jwt



def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id = payload.get("id")
        return id
    except ExpiredSignatureError:
        raise HTTPException(
        status_code=401,
        detail="Please Log In Again.",
        headers={"WWW-Authenticate": "Bearer"},
    )