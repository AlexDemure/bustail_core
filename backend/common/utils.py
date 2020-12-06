import csv
from datetime import timedelta

from fastapi import status
from fastapi_auth.security import create_access_token, create_cookie
from starlette.responses import Response

from backend.core.config import settings


def response_with_token(account_id: int) -> Response:
    """Получение респонса с токеном-авторизации"""
    token = create_access_token(
        subject=str(account_id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response = create_cookie(token)
    response.status_code = status.HTTP_204_NO_CONTENT

    return response


def read_csv_file(file_path: str, ignore_first_line: bool = True) -> list:
    """Получение содержимого csv-файла."""
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = [x for x in csv_reader]
        if ignore_first_line:
            return rows[1:]

        return rows


def get_cities() -> list:
    """Получение списка городов России из списка."""
    path = f'../static/cities.csv'
    cities = read_csv_file(path)
    return [x[2] for x in cities]  # x[2] - Индекс №2 отвечает за столбец "Название города"
