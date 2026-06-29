"""
screen.py

Administración de la pantalla principal.
"""

from __future__ import annotations

import curses

from tui.theme import initialize


class Screen:

    def __init__(self):

        self.window = None

    # -------------------------------------------------

    def start(self):

        self.window = curses.initscr()

        curses.noecho()

        curses.cbreak()

        self.window.keypad(True)

        if curses.has_colors():

            curses.start_color()

            initialize()

        return self.window

    # -------------------------------------------------

    def stop(self):

        if self.window is None:

            return

        self.window.keypad(False)

        curses.echo()

        curses.nocbreak()

        curses.endwin()

    # -------------------------------------------------

    def clear(self):

        self.window.clear()

    # -------------------------------------------------

    def refresh(self):

        self.window.refresh()

    # -------------------------------------------------

    def size(self):

        return self.window.getmaxyx()

    # -------------------------------------------------

    def key(self):

        return self.window.getch()

    # -------------------------------------------------

    def print(
        self,
        y,
        x,
        text,
        color=0,
        attr=0,
    ):

        try:

            if color:

                attr |= curses.color_pair(color)

            self.window.addstr(
                y,
                x,
                text,
                attr,
            )

        except curses.error:

            pass

    # -------------------------------------------------

    def hline(
        self,
        y,
        x,
        length,
    ):

        try:

            self.window.hline(
                y,
                x,
                curses.ACS_HLINE,
                length,
            )

        except curses.error:

            pass

    # -------------------------------------------------

    def vline(
        self,
        y,
        x,
        length,
    ):

        try:

            self.window.vline(
                y,
                x,
                curses.ACS_VLINE,
                length,
            )

        except curses.error:

            pass
