import os

# openssl rand -hex 32
AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", None)

TOKEN_DOMAIN = os.environ.get("AUTH_DOMAIN", 'localhost')

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 720
