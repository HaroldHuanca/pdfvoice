"""
Administrador de motores TTS.
"""

import utils

from .piper_engine import PiperEngine


class TTSManager:

    def __init__(self, audio_dir):

        self.engine = PiperEngine(audio_dir)

    def generate(self, chapter):

        utils.info(f"Capítulo {chapter.number}")

        return self.engine.generate(chapter)

    def generate_all(self, chapters):

        for chapter in chapters:

            self.generate(chapter)
