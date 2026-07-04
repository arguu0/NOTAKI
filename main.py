from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from models import Note, Notes, User
from database import create_db, engine
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

# upd/del - helper
def fetch_note(session: Session, id: int) -> Note:
    statement = select(Notes).where(Notes.id == id)
    result = session.exec(statement)
    return result.one()

#POST method for creating
@app.post("/notes")
def add_note(note: Note):
    note = Notes(note = note.note, time = time.ctime())
    with Session(engine) as session:
        session.add(note)  
        session.commit()   
        session.refresh(note)
        return f"Note added successfully: {note.note}"

#GET method for reading
@app.get("/notes", response_model=list[Notes])
def display_note():
    with Session(engine) as session:
        statement = select(Notes)
        results = session.exec(statement)
        note = results.all()
        return note
    
#PUT method for updating 
@app.put("/notes/{id}")
def edit_note(new_note: Note, id: int):
    with Session(engine) as session:
        note = fetch_note(session, id)  # call fetch_note func
        note.note = new_note.note  # this is the newly added note
        note.time = time.ctime()
        session.add(note)
        session.commit()
        session.refresh(note)
        return f"Updated Note: {note.note}"

#DELETE method for deleting
@app.delete("/notes/{id}")
def del_note(id: int):
    with Session(engine) as session:
        note = fetch_note(session, id)  
        session.delete(note)
        session.commit()
        return f"deleted note: {note.note}"
    
@app.post('/register')
async def register_user(user: User):
    return user