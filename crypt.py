from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Получение пароля ввиде хеша."""
    return pwd_context.hash(password)


def get_verify_code(hash_password) -> str:
    """Получения кода для восстановления на основе hash пароля."""
    return hash_password[1:12:2]
