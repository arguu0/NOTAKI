from pwdlib import PasswordHash
from datetime import time, datetime, timezone, timedelta
from jwt import ExpiredSignatureError
import jwt
from main import HTTPException

pwd_hasher = PasswordHash.recommended()
secret_key = "03f2a4e683d7b71772a13b9b455886ecd32a61d70538797fc0c225daecef2576"
algorithm = "HS256"

def hashed(raw_pwd):
    return pwd_hasher.hash(raw_pwd)

def pwd_verify(hashed_pwd, raw_pwd):
    return pwd_hasher.verify(raw_pwd, hashed_pwd)

def create_token(user_id):
    payload = {"id": user_id}
    payload.update(exp=datetime.now(timezone.utc) + timedelta(minutes=1))
    print(payload)
    encode_jwt = jwt.encode(payload, secret_key, algorithm)
    return encode_jwt

def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        id = payload.get("id")
        return id
    except ExpiredSignatureError:
        raise HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )