from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from models import Note, Notes, User, Users, Note_output
from database import create_db, get_session, get_user_pwd, fetch_note, get_target_id, get_target_detail
from authentication import hashed, pwd_verify, create_token, decode_token
import time
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Allows specific origins (or use ["*"] for all)
    allow_credentials=False,          # Allows cookies or authentication headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all headers
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

create_db()

# -- Register User --
@app.post('/register')
def register_user(user: User, session: Session=Depends(get_session)):
    if not get_target_detail(session, user.username, user.email):
        user = Users(username=user.username, email=user.email, password=hashed(user.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return "Account Created:", user.username
    raise HTTPException(status_code=409, detail="Email or Username already Existed")

@app.post('/login')
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session=Depends(get_session)):
    email = user.username
    hashed_pwd = get_user_pwd(email, session)
    user_id = get_target_id(session, email)
    if not hashed_pwd:
        raise HTTPException(status_code= 404, detail="No User Found")
    is_verified = pwd_verify(hashed_pwd, user.password)
    if is_verified:
        encode_jwt = create_token(user_id)
        return {'access_token': encode_jwt, 'token_type': "bearer"}
    raise HTTPException( status_code=403, detail="Incorrect Password")

#POST method for creating
@app.post("/notes")
def add_note(token: Annotated[str, Depends(oauth2_scheme)], note: Note, session: Session=Depends(get_session)):
    user_id = decode_token(token)
    note = Notes(note = note.note, time = time.ctime(), user_id=user_id)
    session.add(note)  
    session.commit()   
    session.refresh(note)
    return f"Note added successfully: {note.note}"

#GET method for reading
@app.get("/notes", response_model=list[Note_output])
def display_note(token: Annotated[str, Depends(oauth2_scheme)], session: Session=Depends(get_session)):
    user_id = decode_token(token)
    statement = select(Notes).where(Notes.user_id == user_id)
    results = session.exec(statement)
    note = results.all()
    return note
    
#PUT method for updating 
@app.put("/notes/{id}")
def edit_note(note: Annotated[str, Depends(oauth2_scheme)], new_note: Note, id: int, session: Session=Depends(get_session)):
    note = fetch_note(session, id)  # call fetch_note func
    note.note = new_note.note  # this is the newly added note
    note.time = time.ctime()
    session.add(note)
    session.commit()
    session.refresh(note)
    return f"Updated Note: {note.note}"

#DELETE method for deleting
@app.delete("/notes/{id}")
def del_note(note: Annotated[str, Depends(oauth2_scheme)], id: int, session: Session=Depends(get_session)):
    note = fetch_note(session, id)  
    session.delete(note)
    session.commit()
    return f"deleted note: {note.note}"