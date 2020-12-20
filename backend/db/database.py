import databases
from sqlalchemy import create_engine
from backend.core.config import settings
from backend.db.base_class import Base

if settings.ENV == "DEV":
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)


def init_db():
    Base.metadata.create_all(engine)
