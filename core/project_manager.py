"""
project_manager.py

Coordina todo el flujo del proyecto.
"""

from pathlib import Path

import config
import utils

from core.project import Project
from core.extractor import PDFExtractor
from core.splitter import ChapterSplitter
from core.chapter_writer import ChapterWriter


class ProjectManager:

    def __init__(self, pdf_file):

        self.pdf_file = Path(pdf_file)

    # --------------------------------------------------

    def prepare(self):

        utils.info("Preparando proyecto...")

        extractor = PDFExtractor(self.pdf_file)

        text_file = extractor.extract()

        splitter = ChapterSplitter(text_file)

        splitter.load()

        splitter.detect()

        chapters = splitter.build()

        cache_dir = text_file.parent

        chapters_dir = cache_dir / "chapters"

        audio_dir = cache_dir / "audio"

        chapters_dir.mkdir(exist_ok=True)

        audio_dir.mkdir(exist_ok=True)

        writer = ChapterWriter(chapters_dir)

        writer.write(chapters)

        project = Project(

            pdf_file=self.pdf_file,

            cache_dir=cache_dir,

            text_file=Path(text_file),

            chapters_dir=chapters_dir,

            audio_dir=audio_dir,

            chapters=chapters,

            ready=True

        )

        utils.ok("Proyecto listo.")

        return project
