"""
chapter_writer.py

Guarda los capítulos detectados en archivos individuales.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import utils

from core.logger import get_logger

from core.models import Chapter


class ChapterWriter:

    def __init__(self, output_dir: str | Path):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    # --------------------------------------------------------

    def sanitize(self, text: str) -> str:
        """
        Convierte un título en un nombre de archivo válido.
        """

        text = text.strip()

        text = re.sub(r"[^\w\s-]", "", text)

        text = re.sub(r"\s+", "_", text)

        return text[:80]

    # --------------------------------------------------------

    def write(self, chapters: list[Chapter]):

        get_logger().info("Guardando capítulos...")

        index = []

        for chapter in chapters:

            filename = (
                f"{chapter.number:03d}_"
                f"{self.sanitize(chapter.title)}.txt"
            )

            path = self.output_dir / filename

            path.write_text(
                chapter.text,
                encoding="utf-8"
            )

            chapter.filename = path

            index.append({

                "number": chapter.number,

                "title": chapter.title,

                "file": filename,

                "words": chapter.words,

                "characters": chapter.characters,

                "start_line": chapter.start_line,

                "end_line": chapter.end_line,

            })

            get_logger().ok(filename)

        # -------------------------------------

        with open(
            self.output_dir / "index.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                index,
                f,
                indent=4,
                ensure_ascii=False
            )

        get_logger().ok("index.json generado.")
