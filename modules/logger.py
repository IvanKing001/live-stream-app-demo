import logging
from config import LOG_FILE

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.propagate = False
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger