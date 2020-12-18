from enum import Enum


class AccountErrors(Enum):

    phone_already_exist = "Телефон уже используется в системе."
    email_already_exist = "Почта уже используется в системе."
    account_not_found = "Пользователь не найден."
    forbidden = "Доступ запрещен."
    city_not_found = "Город не найден."
    confirmed_code_is_not_found = "Не правильный код подтверждения."
    url_change_password_is_wrong = "Ссылка для смены пароля истекла получите новую ссылку."
    account_is_confirmed = "Аккаунт был ранее подтвержден."
