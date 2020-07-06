import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from db.settings import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_CONTAINER_NAME


# DATABASE_URL = postgresql+psycopg2://{user}:{password}@{host}:{port}
SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_CONTAINER_NAME}:5432/{POSTGRES_DB}'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:bustail@localhost:5432/bustail'

database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
