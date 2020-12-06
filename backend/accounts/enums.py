from enum import Enum


class AccountErrors(Enum):

    phone_already_exist = "Телефон уже используется в системе."
    account_not_found = "Пользователь не найден."
    forbidden = "Доступ запрещен."
    city_not_found = "Город не найден."