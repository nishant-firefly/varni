# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'user', 'password', 'postgres', and 'mydatabase' with your actual PostgreSQL credentials and database name


SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@db:5432/mydatabase"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
