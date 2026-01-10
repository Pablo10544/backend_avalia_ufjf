import logging
from logging.handlers import RotatingFileHandler
import os

class _LoggerSingleton:
    _initialized = False

    @classmethod
    def get_logger(cls):
        logger = logging.getLogger("backend_avalia_ufjf")

        if cls._initialized:
            return logger

        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
            )

            console = logging.StreamHandler()
            console.setFormatter(formatter)

            os.makedirs("logs", exist_ok=True)

            file = RotatingFileHandler(
                "logs/app.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=5
            )
            file.setFormatter(formatter)

            logger.addHandler(console)
            logger.addHandler(file)

        cls._initialized = True
        return logger


# Exposição pública (singleton)
log = _LoggerSingleton.get_logger()
