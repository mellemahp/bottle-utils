#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Logging Utilities

"""
import logging
import structlog
import sys


def configure_logging(log_level=logging.INFO):
    """Configure a structlog logger

    Args:
        log_level (structlog.LogLevel): log level of messages to log

    """
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
    """Mixin to create automatically create a loggler for a class

    Example usage:
    ```
    class MyCoolClass(LogMixin):

        def my_cool_function_with_logging(self):

            self.log.info("Logging is cool!")
    ```

    """

    @property
    def log(self):
        """Cached logger"""
        name = self.__class__.__name__
        return structlog.get_logger(name)
