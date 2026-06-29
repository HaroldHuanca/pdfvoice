"""
layout.py

Calcula la distribución de la interfaz.
"""

from dataclasses import dataclass


@dataclass
class Area:

    y: int

    x: int

    height: int

    width: int


class Layout:

    HEADER_HEIGHT = 3

    STATUS_HEIGHT = 2

    HELP_HEIGHT = 2

    def __init__(self):

        self.header = None

        self.content = None

        self.status = None

        self.help = None

    # -------------------------------------------------

    def update(
        self,
        rows,
        cols,
    ):

        self.header = Area(

            0,

            0,

            self.HEADER_HEIGHT,

            cols,

        )

        content_y = self.HEADER_HEIGHT

        content_h = (

            rows

            - self.HEADER_HEIGHT

            - self.STATUS_HEIGHT

            - self.HELP_HEIGHT

        )

        self.content = Area(

            content_y,

            0,

            content_h,

            cols,

        )

        status_y = content_y + content_h

        self.status = Area(

            status_y,

            0,

            self.STATUS_HEIGHT,

            cols,

        )

        help_y = status_y + self.STATUS_HEIGHT

        self.help = Area(

            help_y,

            0,

            self.HELP_HEIGHT,

            cols,

        )

    # -------------------------------------------------

    def all(self):

        return {

            "header": self.header,

            "content": self.content,

            "status": self.status,

            "help": self.help,

        }
