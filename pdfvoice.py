"""
pdfvoice.py

Fachada principal del proyecto PDFVoice.
"""

from __future__ import annotations

from pathlib import Path

import utils

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

        return self.project.chapters

    # ---------------------------------------------------------

    def list(self): 
        """listar"""

    # ---------------------------------------------------------

    def generate(self, number):

        chapter = self.project[number]

        self.tts.generate(chapter)

        return chapter.audio_file

    # ---------------------------------------------------------

    def generate_all(self):

        self.tts.generate_all(
            self.project.chapters
        )

    # ---------------------------------------------------------

    def play(self, number):

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

        self.player.pause()

    # ---------------------------------------------------------

    def resume(self):

        self.player.resume()

    # ---------------------------------------------------------

    def stop(self):

        self.player.stop()

    # ---------------------------------------------------------

    def next(self):

        chapter = self.project.next()

        self.play(chapter.number)

    # ---------------------------------------------------------

    def previous(self):

        chapter = self.project.previous()

        self.play(chapter.number)

    # ---------------------------------------------------------

    def restart(self):

        self.player.restart()

    # ---------------------------------------------------------

    def seek(self, seconds):

        self.player.seek(seconds)

    # ---------------------------------------------------------

    def speed(self, value):

        self.player.speed(value)

    # ---------------------------------------------------------

    def volume(self, value):

        self.player.volume(value)

    # ---------------------------------------------------------

    def status(self):

        return self.player.status()

    # ---------------------------------------------------------

    def current(self):

        return self.project.current()

    # ---------------------------------------------------------

    def summary(self):

        self.project.summary()

    # ---------------------------------------------------------

    def close(self):

        self.player.quit()
