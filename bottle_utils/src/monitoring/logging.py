#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Logging Utilities

"""
import logging
import structlog
import sys


def configure_logging(log_level=logging.INFO):
    logging.basicConfig(level=log_level, format="%(message)s", stream=sys.stdout)

    processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(indent=1, sort_keys=True),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class LogMixin:
    @property
    def log(self):
        name = self.__class__.__name__
        return structlog.get_logger(name)
