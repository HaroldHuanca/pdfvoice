"""
chapterlist.py

Lista de capítulos.
"""

from __future__ import annotations

import curses

from tui.theme import Theme


class ChapterList:

    def __init__(self):

        self.chapters = []

        self.selected = 0

        self.offset = 0

        self.visible_rows = 0

    # -------------------------------------------------

    def set_chapters(self, chapters):

        self.chapters = chapters

    # -------------------------------------------------

    def move_up(self):

        if self.selected > 0:

            self.selected -= 1

        if self.selected < self.offset:

            self.offset = self.selected

    # -------------------------------------------------

    def move_down(self):

        if self.selected < len(self.chapters) - 1:

            self.selected += 1

        visible = self.visible_rows

        if self.selected >= self.offset + visible:

            self.offset = self.selected - visible + 1

    # -------------------------------------------------

    @property
    def current(self):

        if not self.chapters:

            return None

        return self.chapters[self.selected]

    # -------------------------------------------------

    def draw(
        self,
        screen,
        area,
    ):

        self.visible_rows = area.height

        row = 0

        for i in range(

            self.offset,

            len(self.chapters),

        ):

            if row >= area.height:

                break

            chapter = self.chapters[i]

            marker = "▶" if i == self.selected else " "

            text = (

                f"{marker} "

                f"{chapter.number:02d} "

                f"{chapter.title}"

            )

            if i == self.selected:

                screen.print(

                    area.y + row,

                    2,

                    text[: area.width - 4],

                    Theme.SELECTED,

                    curses.A_BOLD,

                )

            else:

                screen.print(

                    area.y + row,

                    2,

                    text[: area.width - 4],

                    Theme.DEFAULT,

                )

            row += 1
