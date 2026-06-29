"""
statusbar.py

Barra inferior de estado.
"""

from __future__ import annotations

import curses

from tui.theme import Theme


class StatusBar:

    def __init__(self):

        self.state = "READY"

        self.position = 0

        self.duration = 0

        self.speed = 1.0

    # -------------------------------------------------

    def update(
        self,
        state,
        position,
        duration,
        speed,
    ):

        self.state = state

        self.position = position

        self.duration = duration

        self.speed = speed

    # -------------------------------------------------

    def _clock(self, seconds):

        if seconds is None:

            return "--:--"

        seconds = int(seconds)

        minutes = seconds // 60

        seconds %= 60

        return f"{minutes:02d}:{seconds:02d}"
    # -------------------------------------------------

    def draw(
        self,
        screen,
        area,
    ):

        screen.hline(

            area.y,

            0,

            area.width,

        )

        left = (

            f"{self.state}"

            f"   "

            f"{self._clock(self.position)}"

            f"/"

            f"{self._clock(self.duration)}"

        )

        right = f"{self.speed:.2f}x"

        screen.print(

            area.y + 1,

            2,

            left,

            Theme.STATUS,

            curses.A_BOLD,

        )

        screen.print(

            area.y + 1,

            area.width - len(right) - 2,

            right,

            Theme.HIGHLIGHT,

        )
