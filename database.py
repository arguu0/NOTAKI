from sqlmodel import SQLModel, create_engine, Session, select
from models import Users, Notes

sqlite_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_name}"
engine = create_engine(sqlite_url, echo=True)    # connect with the database

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def fetch_note(session: Session, id: int):
    statement = select(Notes).where(Notes.id == id)
    result = session.exec(statement)
    return result.one()

def get_target_id(session: Session, type_email):
    statement = select(Users.id).where(Users.email == type_email)
    user_id = session.exec(statement).first()
    return user_id

def get_target_detail(session: Session, type_username, type_email):
    statement = select(Users.username, Users.email).where(Users.username == type_username and Users.email == type_email)
    user_data = session.exec(statement).first()
    if user_data:
        return True
    return False

def get_user_pwd(type_email, session: Session):
    statement = select(Users.password).where(Users.email == type_email)
    h_pwd = session.exec(statement).first()
    return h_pwd

