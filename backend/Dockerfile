# Dockerfile был загружен в dockerhub под название alexdemure/bustail:core
# https://hub.docker.com/layers/134427835/alexdemure/bustail/core/images/sha256-d139d16dbe0a1a2f254d1be28d32c3cbb808aa5776c2f5b6852a50580b73644b?context=explore

FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Alex Demure <alexanderdemure@gmail.com>"

RUN pip install poetry==1.0.10

ADD poetry.lock pyproject.toml /app/backend/

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/backend

RUN poetry install --no-dev

COPY . /app/backend

EXPOSE 7040

CMD ["uvicorn", "core.application:app", "--host", "127.0.0.1", "--port", "7040"]