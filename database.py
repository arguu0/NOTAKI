from sqlmodel import SQLModel, create_engine

sqlite_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_name}"
engine = create_engine(sqlite_url, echo=True)    # connect with the database

def create_db():
    SQLModel.metadata.create_all(engine)