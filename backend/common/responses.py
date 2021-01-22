from fastapi import status

from backend.enums.accounts import AccountErrors

auth_responses = {
    status.HTTP_403_FORBIDDEN: {"description": AccountErrors.forbidden.value},
    status.HTTP_404_NOT_FOUND: {"description": AccountErrors.account_not_found.value}
}
