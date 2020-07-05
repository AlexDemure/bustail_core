from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db.settings import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_CONTAINER_NAME
from db import models

# DATABASE_URL = postgresql+psycopg2://{user}:{password}@{host}:{port}
# SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_CONTAINER_NAME}:5432/{POSTGRES_DB}'
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:bustail@localhost:5432/bustail'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
