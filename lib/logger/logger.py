import logging


class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def info(self, message: str):
        """Log level info"""
        self.logger.info(message)


logger = Logger()
