from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session
from models import Note, Note_output
from database import get_session
from crud import create_note, read_note, update_note, delete_note
from authentication import oauth2_scheme

router = APIRouter()


#POST method for creating
@router.post("/notes")
def Create_note(token: Annotated[str, Depends(oauth2_scheme)], note: Note, session: Session=Depends(get_session)):
    return create_note(token, note, session)

#GET method for reading
@router.get("/notes", response_model=list[Note_output])
def Read_note(token: Annotated[str, Depends(oauth2_scheme)], session: Session=Depends(get_session)):
    return read_note(token, session)


#PUT method for updating 
@router.put("/notes/{id}")
def Upd_note(note: Annotated[str, Depends(oauth2_scheme)], new_note: Note, id: int, session: Session=Depends(get_session)):
    return update_note(note, new_note, id, session)

#DELETE method for deleting
@router.delete("/notes/{id}")
def Del_note(note: Annotated[str, Depends(oauth2_scheme)], id: int, session: Session=Depends(get_session)):
    return delete_note(note, id, session)