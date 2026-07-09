from sqlmodel import SQLModel, Field
from pydantic import BaseModel, AfterValidator
from typing import Annotated
from fastapi import HTTPException



# ========== custom validation ==========

def char_min_length(v: str) -> str:
    word = len(v)
    if word < 1:
        raise HTTPException(status_code=422, detail="Note must have at least one character.")
    return v

def word_max_length(v: str) -> str:
    word_count = len(v.split())
    if word_count > 100:
        raise HTTPException(status_code=422, detail=f"Word limit reached: {word_count}")
    return v.strip()

def empty_note_check(v: str) -> str:
    if v.strip() == "":
        raise HTTPException(status_code=422, detail="Note cannot be empty.")
    return v

def empty_input_user(v: str) -> str:
    if v.strip() == "":
        raise HTTPException(status_code=422, detail="Username cannot be empty.")
    return v
    
def empty_input_email(v: str) -> str:
    if v.strip() == "":
        raise HTTPException(status_code=422, detail="Email cannot be empty.")
    return v
    
def empty_input_pwd(v: str) -> str:
    if v.strip() == "":
        raise HTTPException(status_code=422, detail="Password cannot be empty.")
    return v





# ========== BaseModel ==========

class Note(BaseModel):  # note input
    note : Annotated [str | None, AfterValidator(char_min_length), AfterValidator(word_max_length), AfterValidator(empty_note_check)] = None

class User(BaseModel):  # for sign-up
    username: Annotated [str, AfterValidator(empty_input_user)]
    email: Annotated [str, AfterValidator(empty_input_email)]
    password: Annotated [str, AfterValidator(empty_input_pwd)]

class Note_output(BaseModel):
    id: int
    note: str
    time: str





# ========== SQLModel ==========

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    username: str = Field(index=True)
    email: str = Field(index=True)
    password: str

class Notes(SQLModel, table=True):   # note database
    id: int | None = Field(default=None, primary_key=True) 
    note: str     # can be set Field(index=True) for easier filter when using .where()
    time: str 
    user_id: int | None = Field(default=None, foreign_key="users.id")