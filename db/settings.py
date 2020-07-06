import os

POSTGRES_DB = os.environ.get("POSTGRES_DB", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_CONTAINER_NAME = os.environ.get("POSTGRES_CONTAINER_NAME", "localhost")
