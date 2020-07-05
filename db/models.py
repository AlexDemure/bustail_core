# from datetime import datetime
# from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Enum, Text
# from sqlalchemy.orm import relationship
#
# from db.database import Base, engine
# from db.enum import TransportType


# class Account(Base):
#     __tablename__ = "accounts"
#
#     id = Column(Integer, primary_key=True, index=True)
#     registration_date = Column(DateTime, default=datetime.utcnow)
#
#
# class AuthorizationData(Base):
#     __tablename__ = "authorization_data"
#
#     login = Column(String(12), unique=True)
#     password = Column(String(64))
#
#
# Base.metadata.create_all(bind=engine)


# class Person(Base):
#     __tablename__ = "persons"
#
#     id = Column(Integer, primary_key=True, index=True)
#     account_id = Column(Integer, ForeignKey("accounts.id"))
#     fullname = Column(String(255))
#     phone = Column(String(12), unique=True)
#     email = Column(String(64), nullable=True)
#     birthday = Column(DateTime, nullable=True)
#     city = Column(String(128), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     client = relationship("Client", uselist=False, back_populates='person')
#     driver = relationship("Driver", uselist=False, back_populates='person')
#
#
# class Client(Base):
#     __tablename__ = "clients"
#
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey("persons.id"))
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     person = relationship("Person", back_populates='client')
#     applications = relationship("Application", back_populates="client")
#
#
# class Driver(Base):
#     __tablename__ = "drivers"
#
#     id = Column(Integer, primary_key=True, index=True)
#     person_id = Column(Integer, ForeignKey("persons.id"))
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     applications = relationship("Application", back_populates="driver")
#     transports = relationship("Transport", back_populates="driver")
#     person = relationship("Person", back_populates='driver')
#
#
# class Application(Base):
#     __tablename__ = 'applications'
#
#     id = Column(Integer, primary_key=True, index=True)
#     client_id = Column(Integer, ForeignKey("clients.id"))
#     driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
#     to_go_from = Column(String(255))
#     to_go_to = Column(String(255), nullable=True)
#     to_go_when = Column(DateTime)
#     count_seats = Column(Integer)
#     description = Column(String(1024), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     confirmed_at = Column(DateTime, nullable=True)
#     completed_at = Column(DateTime, nullable=True)
#
#     client = relationship("Client", back_populates="applications")
#     driver = relationship("Driver", back_populates="applications")
#
#
# class Transport(Base):
#     __tablename__ = "transports"
#
#     id = Column(Integer, primary_key=True, index=True)
#     driver_id = Column(Integer, ForeignKey("drivers.id"))
#     type_transport = Column(Enum(TransportType))
#     brand = Column(String(255))
#     model = Column(String(255))
#     count_seats = Column(Integer)
#
#     driver = relationship("Driver", back_populates="transports")
#     files = relationship("File", back_populates='transport')
#
#
# class File(Base):
#     __tablename__ = "files"
#
#     id = Column(Integer, primary_key=True, index=True)
#     transport_id = Column(Integer, ForeignKey("transports.id"))
#     content = Column(String)
#
#     transport = relationship("Transport", back_populates='files')
