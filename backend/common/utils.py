import csv

from backend.core.config import settings


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


def get_current_domain():
    """Получение текущего домена системы."""
    return f"{settings.SERVER}://{settings.DOMAIN}"


def get_current_api():
    """Получение текущего пути к API системы."""
    return f"{get_current_domain()}{settings.API_URL}"
