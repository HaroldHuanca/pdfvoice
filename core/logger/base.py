"""
Logger abstracto.
"""

from abc import ABC, abstractmethod


class BaseLogger(ABC):

    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def ok(self, message):
        pass

    @abstractmethod
    def warn(self, message):
        pass

    @abstractmethod
    def error(self, message):
        pass
