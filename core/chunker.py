"""
chunker.py

Divide capítulos en bloques para el TTS.
"""

from __future__ import annotations

import re

from core.models import Chunk


class ChapterChunker:

    def __init__(self, max_words: int = 600):

        self.max_words = max_words

    def split(self, chapter):

        text = re.sub(r"\s+", " ", chapter.text).strip()

        words = text.split()

        chunks = []

        start = 0

        number = 1

        while start < len(words):

            end = min(start + self.max_words, len(words))

            piece = " ".join(words[start:end])

            chunks.append(

                Chunk(

                    number=number,

                    text=piece,

                    words=len(piece.split()),

                    characters=len(piece),

                )

            )

            number += 1

            start = end

        chapter.chunks = chunks

        return chunks
