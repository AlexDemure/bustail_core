from fastapi import status
from mailing.src.enums import SendGridErrors


responses = {
    status.HTTP_200_OK: {"description": "Message is send"},
    status.HTTP_401_UNAUTHORIZED: {"description": SendGridErrors.not_found.description},
    status.HTTP_403_FORBIDDEN: {"description": SendGridErrors.forbidden.description},
    status.HTTP_404_NOT_FOUND: {"description": SendGridErrors.not_found.description},
    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"description": SendGridErrors.payload_too_large.description},
    status.HTTP_429_TOO_MANY_REQUESTS: {"description": SendGridErrors.too_many_requests.description},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": SendGridErrors.server_unavailable.description},
    status.HTTP_503_SERVICE_UNAVAILABLE: {"description": SendGridErrors.service_not_available.description}
}
