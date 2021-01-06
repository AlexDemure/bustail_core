from enum import Enum


class SendGridErrors(Enum):

    # https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/errors.html

    unauthorized = 401
    forbidden = 403
    not_found = 404
    payload_too_large = 413
    too_many_requests = 429
    server_unavailable = 500
    service_not_available = 503

    @property
    def description(cls):
        if cls is cls.unauthorized:
            return "UNAUTHORIZED"
        elif cls is cls.forbidden:
            return "FORBIDDEN"
        elif cls is cls.not_found:
            return "NOT FOUND"
        elif cls is cls.payload_too_large:
            return "PAYLOAD TOO LARGE"
        elif cls is cls.too_many_requests:
            return "TOO MANY REQUESTS"
        elif cls is cls.server_unavailable:
            return "SERVER UNAVAILABLE"
        elif cls is cls.server_unavailable:
            return "SERVICE NOT AVAILABLE"
