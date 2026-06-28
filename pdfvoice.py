"""
pdfvoice.py

Clase principal de PDFVoice.
"""

from pathlib import Path

from core.extractor import PDFExtractor
from core.splitter import ChapterSplitter
from core.chapter_writer import ChapterWriter
from core.project_manager import ProjectManager

from core.tts.manager import TTSManager

from player.mpv_player import MPVPlayer


class PDFVoice:

    def __init__(self, pdf):

        self.pdf = Path(pdf)

        self.project = None

        self.tts = TTSManager()

        self.player = MPVPlayer()

    # --------------------------------------------------

    def prepare(self):

        print()

        print("Preparando proyecto...")

        extractor = PDFExtractor(self.pdf)

        text_file = extractor.extract()

        splitter = ChapterSplitter(text_file)

        splitter.load()

        splitter.detect()

        splitter.build()

        writer = ChapterWriter(splitter)

        writer.save()

        self.project = ProjectManager(writer.project_dir)

        self.project.load()

        print()

        print("Proyecto listo.")

    # --------------------------------------------------

    def chapters(self):

        return self.project.chapters

    # --------------------------------------------------

    def list(self):

        for chapter in self.project.chapters:

            print(

                f"{chapter.number:02d} - {chapter.title}"

            )

    # --------------------------------------------------

    def generate(self, number):

        chapter = self.project[number]

        self.tts.generate(chapter)

    # --------------------------------------------------

    def play(self, number):

        chapter = self.project[number]

        if not chapter.audio_file.exists():

            self.generate(number)

        self.player.play(chapter.audio_file)

    # --------------------------------------------------

    def pause(self):

        self.player.pause()

    # --------------------------------------------------

    def resume(self):

        self.player.resume()

    # --------------------------------------------------

    def stop(self):

        self.player.stop()

    # --------------------------------------------------

    def next(self):

        self.project.next()

        self.play(self.project.current)

    # --------------------------------------------------

    def previous(self):

        self.project.previous()

        self.play(self.project.current)

    # --------------------------------------------------

    def speed(self, value):

        self.player.speed(value)

    # --------------------------------------------------

    def volume(self, value):

        self.player.volume(value)

    # --------------------------------------------------

    def status(self):

        return self.player.status()

    # --------------------------------------------------

    def close(self):

        self.player.quit()
