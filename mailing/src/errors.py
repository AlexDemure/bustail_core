from mailing.src.enums import SendGridErrors


class SendGridError(BaseException):
    """
    Исключение в логике обработки материалов
    """
    def __init__(self, error_type: SendGridErrors):
        self.error_type = error_type
