"""
input.py

Interpreta las teclas pulsadas por el usuario.
"""

from __future__ import annotations

import curses


class InputHandler:

    MOVE_UP = "MOVE_UP"

    MOVE_DOWN = "MOVE_DOWN"

    PLAY = "PLAY"

    PAUSE = "PAUSE"

    NEXT = "NEXT"

    PREVIOUS = "PREVIOUS"

    SPEED_UP = "SPEED_UP"

    SPEED_DOWN = "SPEED_DOWN"

    SEEK_FORWARD = "SEEK_FORWARD"

    SEEK_BACKWARD = "SEEK_BACKWARD"

    QUIT = "QUIT"

    NONE = "NONE"

    # -----------------------------------------------------

    def read(self, key):

        if key == curses.KEY_UP:

            return self.MOVE_UP

        if key == curses.KEY_DOWN:

            return self.MOVE_DOWN

        if key in (

            curses.KEY_ENTER,

            10,

            13,

        ):

            return self.PLAY

        if key == ord(" "):

            return self.PAUSE

        if key in (

            ord("n"),

            ord("N"),

        ):

            return self.NEXT

        if key in (

            ord("p"),

            ord("P"),

        ):

            return self.PREVIOUS

        if key == ord("+"):

            return self.SPEED_UP

        if key == ord("-"):

            return self.SPEED_DOWN

        if key == curses.KEY_RIGHT:

            return self.SEEK_FORWARD

        if key == curses.KEY_LEFT:

            return self.SEEK_BACKWARD

        if key in (

            ord("q"),

            ord("Q"),

        ):

            return self.QUIT

        return self.NONE
