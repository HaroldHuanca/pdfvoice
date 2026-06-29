"""
pdfvoice.py

Fachada principal del proyecto PDFVoice.
"""

from __future__ import annotations

from pathlib import Path

from core.project_manager import ProjectManager
from core.tts.manager import TTSManager
from core.logger import get_logger

from player.mpv_player import MPVPlayer


class PDFVoice:

    # ---------------------------------------------------------

    def __init__(self, pdf_file):

        self.pdf_file = Path(pdf_file)

        self.project = None

        self.tts = None

        self.player = MPVPlayer()


    # ---------------------------------------------------------

    @property
    def ready(self):

        return self.project is not None

    # ---------------------------------------------------------

    def _ensure_ready(self):

        if not self.ready:

            raise RuntimeError("Proyecto no preparado")

    # ---------------------------------------------------------

    def prepare(self):

        get_logger().info("Abriendo proyecto...")

        manager = ProjectManager(self.pdf_file)

        self.project = manager.prepare()

        self.tts = TTSManager(
            self.project.audio_dir
        )

        get_logger().ok("Proyecto preparado.")

        return self.project

    # ---------------------------------------------------------

    def chapters(self):

        self._ensure_ready()

        return self.project.chapters

    # ---------------------------------------------------------

    def list(self):
        """Devuelve la lista de capítulos preparados."""

        self._ensure_ready()

        return self.project.chapters

    # ---------------------------------------------------------

    def generate(self, number):

        self._ensure_ready()

        chapter = self.project[number]

        self.tts.generate(chapter)

        return chapter.audio_file

    # ---------------------------------------------------------

    def generate_all(self):

        self._ensure_ready()

        self.tts.generate_all(
            self.project.chapters
        )

    # ---------------------------------------------------------

    def play(self, number):

        self._ensure_ready()

        chapter = self.project[number]

        self.project.current_chapter = number - 1

        if (
            chapter.audio_file is None
            or
            not Path(chapter.audio_file).exists()
        ):

            self.generate(number)

        self.player.play(chapter.audio_file)

    # ---------------------------------------------------------

    def pause(self):

        self._ensure_ready()

        self.player.pause()

    # ---------------------------------------------------------

    def resume(self):

        self._ensure_ready()

        self.player.resume()

    # ---------------------------------------------------------

    def stop(self):

        self._ensure_ready()

        self.player.stop()

    # ---------------------------------------------------------

    def next(self):

        self._ensure_ready()

        chapter = self.project.next()

        self.play(chapter.number)

    # ---------------------------------------------------------

    def previous(self):

        self._ensure_ready()

        chapter = self.project.previous()

        self.play(chapter.number)

    # ---------------------------------------------------------

    def restart(self):

        self._ensure_ready()

        self.player.restart()

    # ---------------------------------------------------------

    def seek(self, seconds):

        self._ensure_ready()

        self.player.seek(seconds)

    # ---------------------------------------------------------

    def speed(self, value):

        self._ensure_ready()

        self.player.speed(value)

    # ---------------------------------------------------------

    def volume(self, value):

        self._ensure_ready()

        self.player.volume(value)

    # ---------------------------------------------------------

    def status(self):

        self._ensure_ready()

        return self.player.status()

    # ---------------------------------------------------------

    def current(self):

        self._ensure_ready()

        return self.project.current()

    # ---------------------------------------------------------

    def summary(self):

        self._ensure_ready()

        return self.project.summary()

    # ---------------------------------------------------------

    def close(self):

        self.player.quit()
