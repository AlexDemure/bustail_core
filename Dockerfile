FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Alex Demure <alexanderdemure@gmail.com>"

RUN pip install --no-cache-dir fastapi uvicorn fastapi-sqlalchemy psycopg2 alembic

COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000"]