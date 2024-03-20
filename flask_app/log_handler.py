import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()

formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

# console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# file handler
file_handler = RotatingFileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

