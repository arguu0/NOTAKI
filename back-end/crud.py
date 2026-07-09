import time
from sqlmodel import Session, select
from fastapi import HTTPException
from models import User, Users, Note, Notes
from authentication import hashed, pwd_verify, create_token, decode_token


# -------------------------------------------   Helper functions   ------------------------------------------------

def get_note_by_user_id(user_id, session: Session):
    statement = select(Notes).where(Notes.user_id == user_id)
    notes = session.exec(statement).all()
    return notes

def get_note_by_note_id(id, session: Session):
    statement = select(Notes).where(Notes.id == id)
    notes = session.exec(statement).one()
    return notes

def get_target_id(session: Session, type_email):
    statement = select(Users.id).where(Users.email == type_email)
    user_id = session.exec(statement).first()
    return user_id

def get_user_pwd(type_email, session: Session):
    statement = select(Users.password).where(Users.email == type_email)
    password = session.exec(statement).first()
    return password
  
def delete(note, session: Session):
    session.delete(note)
    session.commit()
    return True

def insert_value_to_database(data, session: Session) -> bool:
    session.add(data)
    session.commit()
    session.refresh(data)
    return True





# -------------------------------------------   Users   ----------------------------------------------

# ======   Register new user   ======
def create_user(user: User, session: Session):   
    statement = select(Users).where((Users.username == user.username) | (Users.email == user.email))    # had to change logical operator from "or" to symbol "|"
    is_taken = session.exec(statement).first()
    if is_taken:
        raise HTTPException(status_code=409, detail="Email or Username already Taken.")
    user = Users(username=user.username, email=user.email, password=hashed(user.password))
    if insert_value_to_database(user, session):
        return "Account Created"


# ======   Login account   ======
def login_account(email, raw_password, session: Session):
    hashed_password = get_user_pwd(email, session)
    if not hashed_password:
        raise HTTPException(status_code=404, detail="No User Found. Please Enter a valid email.")
    is_verified = pwd_verify(raw_password, hashed_password)
    if is_verified:
        user_id = get_target_id(session, email)
        encode_jwt = create_token(user_id)
        return {'access_token': encode_jwt, 'token_type': 'bearer'}
    raise HTTPException(status_code=403, detail="Incorrect Password.")





# --------------------------------------    Notes (CRUD)   --------------------------------------

# =====   Create Note   =====
def create_note(token, note: Note, session: Session):
    user_id = decode_token(token)
    note = Notes(note=note.note, time=time.ctime(), user_id=user_id)
    if insert_value_to_database(note, session):
        return "Your note has been created."


# =====   Read Note   =====
def read_note(token, session: Session):
    user_id = decode_token(token)
    notes = get_note_by_user_id(user_id, session)
    return notes


# =====   Update Note   =====
def update_note(note, new_note, id, session: Session):
    note = get_note_by_note_id(id, session)
    note.note = new_note.note
    note.time = time.ctime()
    if insert_value_to_database(note, session):
        return "Note Updated."


# =====   Delete Note   =====
def delete_note(note, id, session: Session):
    note = get_note_by_note_id(id, session)
    if delete(note, session):
        return "Note Deleted."