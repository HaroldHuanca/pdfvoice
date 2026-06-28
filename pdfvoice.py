"""
pdfvoice.py

Fachada principal de PDFVoice.
"""

from __future__ import annotations

from pathlib import Path

import utils

from core.project_manager import ProjectManager
from core.tts.manager import TTSManager
from player.mpv_player import MPVPlayer


class PDFVoice:

    def __init__(self):

        self.project = None

        self.tts = None

        self.player = MPVPlayer()

        self.current = 0

    # ---------------------------------------------------------

    def open(self, pdf):

        """
        Abre un nuevo proyecto.
        """

        utils.info("Abriendo proyecto...")

        self.project = ProjectManager(pdf).prepare()

        self.tts = TTSManager(self.project.audio_dir)

        self.current = 0

        utils.ok("Proyecto listo.")

    # ---------------------------------------------------------

    @property
    def current_chapter(self):

        return self.project.chapters[self.current]

    # ---------------------------------------------------------

    def play(self):

        """
        Reproduce el capítulo actual.
        """

        chapter = self.current_chapter

        if not chapter.generated:

            utils.info("Generando audio...")

            self.tts.generate(chapter)

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

    def speed(self, value):

        self.player.speed(value)

    # ---------------------------------------------------------

    def next(self):

        if self.current >= len(self.project.chapters) - 1:

            utils.warn("Último capítulo.")

            return

        self.current += 1

        self.play()

    # ---------------------------------------------------------

    def previous(self):

        if self.current == 0:

            utils.warn("Primer capítulo.")

            return

        self.current -= 1

        self.play()

    # ---------------------------------------------------------

    def chapter(self, number):

        """
        Cambia al capítulo indicado.

        number empieza en 1.
        """

        number -= 1

        if number < 0:

            return

        if number >= len(self.project.chapters):

            return

        self.current = number

        self.play()

    # ---------------------------------------------------------

    def chapters(self):

        """
        Devuelve todos los capítulos.
        """

        return self.project.chapters

    # ---------------------------------------------------------

    def info(self):

        chapter = self.current_chapter

        return {

            "chapter": chapter.number,

            "title": chapter.title,

            "audio": chapter.audio_file,

            "generated": chapter.generated,

            "total": len(self.project.chapters),

        }

    # ---------------------------------------------------------

    def close(self):

        self.player.quit()

        utils.ok("Proyecto cerrado.")
