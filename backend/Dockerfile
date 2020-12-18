FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Alex Demure <alexanderdemure@gmail.com>"

ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

ENV PYENV_ROOT="/.pyenv" \
    PATH="/.pyenv/bin:/.pyenv/shims:$PATH" \
    POETRY_VERSION=1.0.5 \
    VIRTUAL_ENV=/opt/venv

RUN apt-get update && apt-get install -y --no-install-recommends make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python-openssl \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN cd /usr/local/src && curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

RUN pyenv update
RUN pyenv install 3.8.3
RUN pyenv global 3.8.3

# Установка менеджера зависимостей poetry в системный Python
RUN pip install "poetry==$POETRY_VERSION"

# Создание и активация нового venv для проекта
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


ADD poetry.lock pyproject.toml /app/backend/

WORKDIR /app/backend

RUN poetry install --no-dev

COPY . /app/backend


WORKDIR /app/backend/core

EXPOSE 8000

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000"]