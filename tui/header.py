"""
header.py

Cabecera de PDFVoice.
"""

from __future__ import annotations

import curses

from tui.theme import Theme


class Header:

    def __init__(self):

        self.filename = ""

        self.chapter_count = 0

    # -------------------------------------------------

    def update(
        self,
        filename,
        chapter_count,
    ):

        self.filename = filename

        self.chapter_count = chapter_count

    # -------------------------------------------------

    def draw(
        self,
        screen,
        area,
    ):

        title = " PDFVoice "

        screen.print(

            area.y,

            2,

            title,

            Theme.HEADER,

            curses.A_BOLD,

        )

        screen.print(

            area.y + 1,

            2,

            f"Documento : {self.filename}",

            Theme.DEFAULT,

        )

        screen.print(

            area.y + 1,

            area.width - 18,

            f"{self.chapter_count} capítulos",

            Theme.STATUS,

        )

        screen.hline(

            area.y + area.height - 1,

            0,

            area.width,

        )
