from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import os


DB_NAME = os.getenv("POSTGRES_DB", "matching_service.db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_NAME}", echo=True)


def get_session():
    with sessionmaker(bind=engine).begin() as session:
        yield session