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

    def _ensure_prepared(self):

        if not self.prepared:
            self.prepare()

    # ---------------------------------------------------------
    # Información
    # ---------------------------------------------------------

    @property
    def project(self):

        self._ensure_prepared()

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

    def current_index(self):

        return self.chapter - 1

    # ---------------------------------------------------------
    # Navegación
    # ---------------------------------------------------------

    def first(self):

        self._ensure_prepared()

        self.chapter = 1

    def last(self):

        self._ensure_prepared()

        self.chapter = self.chapter_count

    def next(self):

        self._ensure_prepared()

        if self.chapter < self.chapter_count:

            self.chapter += 1

    def previous(self):

        self._ensure_prepared()

        if self.chapter > 1:

            self.chapter -= 1

    def goto(self, number):

        self._ensure_prepared()

        if 1 <= number <= self.chapter_count:

            self.chapter = number

    # ---------------------------------------------------------
    # Audio
    # ---------------------------------------------------------

    def generate(self):

        self._ensure_prepared()

        self.app.generate(self.chapter)

    def play(self):

        self._ensure_prepared()

        self.app.play(self.chapter)

    def pause(self):

        self._ensure_prepared()

        self.app.pause()

    def resume(self):

        self._ensure_prepared()

        self.app.resume()

    def stop(self):

        self._ensure_prepared()

        self.app.stop()

    # ---------------------------------------------------------
    # Generación de audio
    # ---------------------------------------------------------

    def generate_chapter(self, number):

        self._ensure_prepared()

        chapter = self.project[number - 1]

        chapter.generating = True

        try:

            self.app.generate(number)

        finally:

            chapter.generating = False

    def generate_missing(self):

        self._ensure_prepared()

        for chapter in self.project.chapters:

            if (
                chapter.audio_file is None
                or not Path(chapter.audio_file).exists()
            ):

                try:

                    self.generate_chapter(chapter.number)

                except Exception:

                    continue

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

        self._ensure_prepared()

        self.app.speed(value)

        self.project.speed = value

    def volume(self, value):

        self._ensure_prepared()

        self.app.volume(value)

    def seek(self, seconds):

        self._ensure_prepared()

        self.app.seek(seconds)

    def restart(self):

        self._ensure_prepared()

        self.app.restart()

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
