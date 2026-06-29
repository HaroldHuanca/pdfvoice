"""
helpbar.py

Barra de ayuda ubicada en la última línea de la pantalla.
"""

from __future__ import annotations

from tui.theme import Theme


class HelpBar:

    def __init__(self):

        self.items = [

            ("↑↓", "Mover"),

            ("Enter", "Reproducir"),

            ("Espacio", "Pausa"),

            ("N", "Siguiente"),

            ("P", "Anterior"),

            ("+", "Velocidad+"),

            ("-", "Velocidad-"),

            ("Q", "Salir"),

        ]

    # -----------------------------------------------------

    def text(self):

        parts = []

        for key, desc in self.items:

            parts.append(f"{key}:{desc}")

        return "   ".join(parts)

    # -----------------------------------------------------

    def draw(self, screen, area):

        text = self.text()

        if len(text) > area.width - 2:

            text = text[: area.width - 5] + "..."

        screen.print(

            area.y,

            area.x,

            text.ljust(area.width),

            Theme.HELP,

        )
