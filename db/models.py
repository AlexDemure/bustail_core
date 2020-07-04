from datetime import datetime
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String, Enum, Table, MetaData

from db.database import engine
from db.enum import TransportType

metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("login", String(12), unique=True),
    Column("password", String(256)),
    Column("registration_date", DateTime, default=datetime.utcnow)
)


# relationship("Client", uselist=False, back_populates='person'),
# relationship("Driver", uselist=False, back_populates='person'),
persons = Table(
    "persons",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("account_id", Integer, ForeignKey("accounts.id"), unique=True),
    Column("fullname", String(128), unique=True),
    Column("phone", String(12), unique=True),
    Column("email", String(64), nullable=True),
    Column("birthday", DateTime, nullable=True),
    Column("city", String(128), nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),

)


# person = relationship("Person", back_populates='client')
# applications = relationship("Application", back_populates="client")
clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("person_id", Integer, ForeignKey("persons.id"), unique=True),
    Column("created_at", DateTime, default=datetime.utcnow)
)


# applications = relationship("Application", back_populates="driver")
# transports = relationship("Transport", back_populates="driver")
# person = relationship("Person", back_populates='driver')
drivers = Table(
    "drivers",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("person_id", Integer, ForeignKey("persons.id"), unique=True),
    Column("created_at", DateTime, default=datetime.utcnow)
)


# client = relationship("Client", back_populates="applications")
# driver = relationship("Driver", back_populates="applications")
applications = Table(
    "applications",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("client_id", Integer, ForeignKey("clients.id")),
    Column("driver_id", Integer, ForeignKey("drivers.id"), nullable=True),
    Column("to_go_from", String(255)),
    Column("to_go_to", String(255), nullable=True),
    Column("to_go_when", DateTime),
    Column("count_seats", Integer),
    Column("description", String(1024), nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("confirmed_at", DateTime, nullable=True),
    Column("completed_at", DateTime, nullable=True)
)


#     driver = relationship("Driver", back_populates="transports")
#     files = relationship("File", back_populates='transport')
transports = Table(
    "transports",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("driver_id", Integer, primary_key=True, index=True),
    Column("type_transport", Enum(TransportType)),
    Column("brand", String(255)),
    Column("model", String(255)),
    Column("count_seats", Integer),

)

metadata.create_all(bind=engine)

#     transport = relationship("Transport", back_populates='files')
# files = Table(
#     "files",
#     metadata,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("transport_id", Integer, ForeignKey("transports.id")),
#     Column("content", String)
# )

