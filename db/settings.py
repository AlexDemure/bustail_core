import os

POSTGRES_DB = os.environ.get("POSTGRES_DB", 'bustail')
POSTGRES_USER = os.environ.get("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'bustail')
POSTGRES_CONTAINER_NAME = os.environ.get("POSTGRES_CONTAINER_NAME", "localhost")
