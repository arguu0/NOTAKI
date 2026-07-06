from sqlmodel import SQLModel, Field
from pydantic import BaseModel, AfterValidator
from pydantic_core import PydanticCustomError
from typing import Annotated

# custom error for min_length
def char_min_length(v: str) -> str:
    word = len(v)
    if word < 1:
        raise PydanticCustomError("invalid_value","Note must have at least one character.")
    return v

# custom error for word_limit
def word_max_length(v: str) -> str:
    word_count = len(v.split())
    if word_count > 100:
        raise PydanticCustomError("word_count_exceed",f"Word limit reached: {word_count}")
    return v.strip()

def empty_note_check(v: str) -> str:
    if v.strip() == "":
        raise PydanticCustomError("empty_note","Note cannot be empty")
    return v

class Note(BaseModel):
    note : Annotated [str | None, AfterValidator(char_min_length), AfterValidator(word_max_length), AfterValidator(empty_note_check)] = None

class Notes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    note: str     # can be set Field(index=True) for easier filter when using .where()
    time: str 

class User(BaseModel):  # for sign-up
    username: str
    email: str
    password: str

class User_login(BaseModel): # for login
    email: str
    password: str

class login_output(BaseModel):
    email: str
    password: str

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True) 
    user_id: int | None = Field(default=None, foreign_key="notes.id")
    username: str
    email: str
    password: str