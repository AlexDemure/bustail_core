FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Alex Demure <alexanderdemure@gmail.com>"

RUN pip install poetry==1.0.10

ADD poetry.lock pyproject.toml /app/backend/

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/backend

RUN poetry install --no-dev

COPY . /app/backend

EXPOSE 7040
