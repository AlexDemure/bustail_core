import databases
from sqlalchemy import create_engine
from backend.core.config import settings

database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
