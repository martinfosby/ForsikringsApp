import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler("app.log")
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
