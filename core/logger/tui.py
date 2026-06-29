"""
Logger para la TUI.
"""

from .base import BaseLogger


class TUILogger(BaseLogger):

    def __init__(self):

        self.message = ""

    def _set(self, text):

        self.message = text

    def info(self, msg):

        self._set(msg)

    def ok(self, msg):

        self._set(msg)

    def warn(self, msg):

        self._set(msg)

    def error(self, msg):

        self._set(msg)
