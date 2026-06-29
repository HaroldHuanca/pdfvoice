"""
theme.py

Define todos los colores utilizados por la interfaz.
"""

import curses


class Theme:

    DEFAULT = 1

    HEADER = 2

    STATUS = 3

    HELP = 4

    SELECTED = 5

    HIGHLIGHT = 6

    ERROR = 7

    SUCCESS = 8


def initialize():
    """
    Inicializa todos los colores.
    """

    curses.start_color()

    curses.use_default_colors()

    curses.init_pair(
        Theme.DEFAULT,
        curses.COLOR_WHITE,
        -1,
    )

    curses.init_pair(
        Theme.HEADER,
        curses.COLOR_CYAN,
        -1,
    )

    curses.init_pair(
        Theme.STATUS,
        curses.COLOR_GREEN,
        -1,
    )

    curses.init_pair(
        Theme.HELP,
        curses.COLOR_YELLOW,
        -1,
    )

    curses.init_pair(
        Theme.SELECTED,
        curses.COLOR_BLACK,
        curses.COLOR_CYAN,
    )

    curses.init_pair(
        Theme.HIGHLIGHT,
        curses.COLOR_MAGENTA,
        -1,
    )

    curses.init_pair(
        Theme.ERROR,
        curses.COLOR_RED,
        -1,
    )

    curses.init_pair(
        Theme.SUCCESS,
        curses.COLOR_GREEN,
        -1,
    )
