"""
Sourced from https://signoz.io/guides/python-logging-best-practices/#4-centralize-your-logging-configuration
"""

import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z"
        },
    },
    # handler accepts everything
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
    },
    # root logger decides what appears
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)