from pwdlib import PasswordHash

pwd_hasher = PasswordHash.recommended()

def hashed(raw_pwd):
    return pwd_hasher.hash(raw_pwd)

def verify_pwd(raw_pwd, hashed_pwd):
    return pwd_hasher.verify(raw_pwd, hashed_pwd)
