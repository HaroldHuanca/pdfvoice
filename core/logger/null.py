"""
Logger silencioso.
"""

from .base import BaseLogger


class NullLogger(BaseLogger):

    def info(self, msg):
        pass

    def ok(self, msg):
        pass

    def warn(self, msg):
        pass

    def error(self, msg):
        pass
