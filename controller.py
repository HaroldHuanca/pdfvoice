"""
controller.py

Controlador principal de PDFVoice.

Las interfaces (CLI, TUI, GUI) únicamente hablan con esta clase.
"""

from __future__ import annotations

from pathlib import Path

from pdfvoice import PDFVoice


class Controller:

    def __init__(self, pdf: str | Path):

        self.pdf = Path(pdf)

        self.app = PDFVoice(self.pdf)

        self.chapter = 1

        self.prepared = False

    # ---------------------------------------------------------
    # Proyecto
    # ---------------------------------------------------------

    def prepare(self):

        if self.prepared:
            return

        self.app.prepare()

        self.prepared = True

    # ---------------------------------------------------------
    # Información
    # ---------------------------------------------------------

    @property
    def project(self):

        return self.app.project

    @property
    def chapters(self):

        return self.project.chapters

    @property
    def chapter_count(self):

        return len(self.project.chapters)

    def current_chapter(self):

        return self.chapter

    def current(self):

        return self.project.chapters[self.chapter - 1]

    # ---------------------------------------------------------
    # Navegación
    # ---------------------------------------------------------

    def first(self):

        self.chapter = 1

    def last(self):

        self.chapter = self.chapter_count

    def next(self):

        if self.chapter < self.chapter_count:

            self.chapter += 1

    def previous(self):

        if self.chapter > 1:

            self.chapter -= 1

    def goto(self, number):

        if 1 <= number <= self.chapter_count:

            self.chapter = number

    # ---------------------------------------------------------
    # Audio
    # ---------------------------------------------------------

    def generate(self):

        self.app.generate(self.chapter)

    def play(self):

        self.app.play(self.chapter)

    def pause(self):

        self.app.pause()

    def resume(self):

        self.app.resume()

    def stop(self):

        self.app.stop()

    # ---------------------------------------------------------
    # Reproducción continua
    # ---------------------------------------------------------

    def play_next(self):

        self.next()

        self.play()

    def play_previous(self):

        self.previous()

        self.play()

    # ---------------------------------------------------------
    # Propiedades
    # ---------------------------------------------------------

    def speed(self, value):

        self.app.speed(value)

    def volume(self, value):

        self.app.volume(value)

    # ---------------------------------------------------------
    # Estado
    # ---------------------------------------------------------

    def status(self):

        return self.app.status()

    @property
    def state(self):

        return self.status()["state"]

    @property
    def position(self):

        return self.status()["position"]

    @property
    def duration(self):

        return self.status()["duration"]

    @property
    def speed_value(self):

        return self.status()["speed"]

    @property
    def volume_value(self):

        return self.status()["volume"]

    # ---------------------------------------------------------
    # Información del capítulo actual
    # ---------------------------------------------------------

    @property
    def title(self):

        return self.current().title

    @property
    def filename(self):

        return self.current().filename

    @property
    def audio(self):

        return self.current().audio_file

    # ---------------------------------------------------------
    # Cierre
    # ---------------------------------------------------------

    def close(self):

        self.app.close()
