"""
Administrador de motores TTS.
"""

from .piper_engine import PiperEngine
from core.logger import get_logger


class TTSManager:

    def __init__(self, audio_dir):

        self.engine = PiperEngine(audio_dir)


    def generate(self, chapter):

        get_logger().info(f"Capítulo {chapter.number}")

        return self.engine.generate(chapter)

    def generate_all(self, chapters):

        for chapter in chapters:

            self.generate(chapter)
