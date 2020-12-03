from sqlalchemy import Column, Integer, String, Enum

from app.db.base_class import Base
from app.sqlalchemy_roles_and_permissions.enums import Permissions


class Permission(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(128), Enum(Permissions), unique=True)
    description = Column(String(128))