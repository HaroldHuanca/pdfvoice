"""
project.py

Representa un proyecto PDFVoice completo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from core.models import Chapter


@dataclass
class Project:

    # -------------------------
    # Archivo original
    # -------------------------

    pdf_file: Path

    # -------------------------
    # Directorio cache
    # -------------------------

    cache_dir: Path

    # -------------------------
    # texto.txt
    # -------------------------

    text_file: Path

    # -------------------------
    # chapters/
    # -------------------------

    chapters_dir: Path

    # -------------------------
    # audio/
    # -------------------------

    audio_dir: Path

    # -------------------------

    chapters: list[Chapter] = field(default_factory=list)

    # -------------------------

    title: str = ""

    author: str = ""

    language: str = "es"

    # -------------------------

    current_chapter: int = 0

    speed: float = 1.0

    # -------------------------

    ready: bool = False

    # -------------------------

    @property
    def chapter_count(self):

        return len(self.chapters)

    # -------------------------

    @property
    def total_words(self):

        return sum(c.words for c in self.chapters)

    # -------------------------

    @property
    def total_characters(self):

        return sum(c.characters for c in self.chapters)

    # -------------------------

    def summary(self):

        print()

        print("=" * 60)

        print("Proyecto")

        print("=" * 60)

        print("PDF:", self.pdf_file.name)

        print("Capítulos:", self.chapter_count)

        print("Palabras:", self.total_words)

        print("Caracteres:", self.total_characters)

        print("Idioma:", self.language)

        print("=" * 60)
