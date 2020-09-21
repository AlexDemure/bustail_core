from sqlalchemy import DateTime, Enum, Column, Integer, String, ForeignKey, Date
from sqlalchemy.sql import func

from accounts.enums import Roles, Permissions
from db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), Enum(Roles), unique=True)
    description = Column(String(128), Enum(Roles))


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), Enum(Permissions), unique=True)
    description = Column(String(128), Enum(Roles))


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))


class AccountRole(Base):
    __tablename__ = "accounts_role"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    registration_date = Column(DateTime, server_default=func.now())


class AuthorizationData(Base):
    __tablename__ = "authorization_data"

    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True, index=True)
    login = Column(String(12), unique=True)
    password = Column(String(64))


class PersonalData(Base):
    __tablename__ = "personal_data"

    account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True, index=True)
    fullname = Column(String(255))
    phone = Column(String(12))
    email = Column(String(64), nullable=True)
    birthday = Column(Date, nullable=True)
    city = Column(String(128))


roles = Role.__table__
permissions = Permission.__table__
role_permissions = RolePermission.__table__
accounts_role = AccountRole.__table__
accounts = Account.__table__
personal_data = PersonalData.__table__
authorization_data = AuthorizationData.__table__