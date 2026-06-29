"""
Logger global.
"""

from .console import ConsoleLogger

_logger = ConsoleLogger()


def set_logger(logger):

    global _logger

    _logger = logger


def get_logger():

    return _logger
