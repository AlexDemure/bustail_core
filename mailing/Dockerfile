FROM python:3.8


RUN pip install poetry==1.0.10

WORKDIR /app/mailing

COPY poetry.lock pyproject.toml /app/mailing/

ENV POETRY_VIRTUALENVS_CREATE=false

RUN poetry install --no-dev

COPY . /app/mailing

WORKDIR /app/

CMD ["uvicorn", "mailing.src.core.application:app", "--host", "127.0.0.1", "--port", "8001"]