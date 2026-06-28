"""
models.py

Modelos utilizados por PDFVoice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Chapter:
    """
    Representa un capítulo del documento.
    """

    number: int

    title: str

    text: str

    filename: Path | None = None

    start_line: int = 0

    end_line: int = 0

    pages: list[int] | None = None

    duration: float = 0.0

    audio_file: str | None = None

    audio_duration: float = 0.0

    generated: bool = False

    chunks: list[Chunk] = field(default_factory=list)

    def __str__(self):

        return f"{self.number:03d} - {self.title}"

    @property
    def words(self):

        return len(self.text.split())

    @property
    def characters(self):

        return len(self.text)

@dataclass
class Chunk:

    number: int

    text: str

    words: int

    characters: int

    audio_file: str | None = None

    generated: bool = False
