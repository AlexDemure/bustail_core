FROM python:3.8


RUN pip install poetry==1.0.10

WORKDIR /app/backend

COPY poetry.lock pyproject.toml /app/backend/

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-dev

COPY . /app/backend

WORKDIR /app/

CMD ["uvicorn", "backend.core.application:app", "--host", "127.0.0.1", "--port", "8002"]