from structlog import get_logger


class BaseService:
    schema = None

    logger = None

    def __init__(self, schema):
        self.schema = schema
        self.logger = get_logger()
