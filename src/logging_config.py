import logging
import logging.config
from logging.handlers import RotatingFileHandler


def setup_logging(log_level=logging.INFO):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "../app.log",
                "level": log_level,
                "maxBytes": 10 * 1024 * 1024,  # 10 Mo
                #'backupCount': 3,  # Garder 3 fichiers de sauvegarde
            },
        },
        "root": {
            "handlers": ["file"],
            "level": log_level,
        },
    }
    logging.config.dictConfig(logging_config)
