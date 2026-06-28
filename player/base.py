"""
Interfaz del reproductor.
"""

from abc import ABC, abstractmethod


class BasePlayer(ABC):

    @abstractmethod
    def play(self, audio):
        ...

    @abstractmethod
    def pause(self):
        ...

    @abstractmethod
    def resume(self):
        ...

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def speed(self, value):
        ...

    @abstractmethod
    def seek(self, seconds):
        ...
