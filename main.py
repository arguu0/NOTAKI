from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from models import Note, Notes, User, Users, User_login
from database import create_db, engine, get_session, get_user_pwd, fetch_note
from pwd_hash import hashed, verify_pwd
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Allows specific origins (or use ["*"] for all)
    allow_credentials=False,          # Allows cookies or authentication headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all headers
)

create_db()

#POST method for creating
@app.post("/notes")
def add_note(note: Note, session: Session=Depends(get_session)):
    note = Notes(note = note.note, time = time.ctime())
    session.add(note)  
    session.commit()   
    session.refresh(note)
    return f"Note added successfully: {note.note}"

#GET method for reading
@app.get("/notes", response_model=list[Notes])
def display_note(session: Session=Depends(get_session)):
    statement = select(Notes)
    results = session.exec(statement)
    note = results.all()
    return note
    
#PUT method for updating 
@app.put("/notes/{id}")
def edit_note(new_note: Note, id: int, session: Session=Depends(get_session)):
    note = fetch_note(session, id)  # call fetch_note func
    note.note = new_note.note  # this is the newly added note
    note.time = time.ctime()
    session.add(note)
    session.commit()
    session.refresh(note)
    return f"Updated Note: {note.note}"

#DELETE method for deleting
@app.delete("/notes/{id}")
def del_note(id: int, session: Session=Depends(get_session)):
    note = fetch_note(session, id)  
    session.delete(note)
    session.commit()
    return f"deleted note: {note.note}"

# -- Register User --
@app.post('/register')
def register_user(user: User, session: Session=Depends(get_session)):
    user = Users(username=user.username, email=user.email, password=hashed(user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post('/login')
def login(user: User_login, session: Session=Depends(get_session)):
    hashed_pwd = get_user_pwd(user, session)
    if not hashed_pwd:
        raise HTTPException(
            status_code= 404,
            detail="No User Found")
    v_pwd = verify_pwd(user.password, hashed_pwd)
    if v_pwd:
        return "Login Succeed"
    return "Login Failed"