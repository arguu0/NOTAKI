from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session
from models import User
from database import get_session
from crud import create_user, login_account
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# -- Register User --
@router.post('/register')
def register_user(user: User, session: Session=Depends(get_session)):
    return create_user(user, session)

# -- Login Account --
@router.post('/login')
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session=Depends(get_session)):
    email = user.username   # oauth2reqform only support username, so i set username as email
    return login_account(email, user.password, session)