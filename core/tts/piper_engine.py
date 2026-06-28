"""
piper_engine.py

Motor TTS basado en Piper.
"""

from pathlib import Path
import subprocess

import config
import utils

from core.models import Chapter
from core.chunker import ChapterChunker
from .base import BaseTTSEngine


class PiperEngine(BaseTTSEngine):

    def __init__(self, output_dir):

        super().__init__(output_dir)

        self.chunker = ChapterChunker()

    # ----------------------------------------------------

    def generate(self, chapter: Chapter):

        """
        Genera el audio completo del capítulo.
        """

        self._prepare(chapter)

        self._generate_chunks(chapter)

        final_audio = self._merge_chunks(chapter)

        self._update(chapter, final_audio)

        return final_audio

    # ----------------------------------------------------

    def _prepare(self, chapter):

        """
        Prepara el directorio y divide el capítulo.
        """

        if not chapter.chunks:

            self.chunker.split(chapter)

        self.chapter_dir = self.output_dir / f"{chapter.number:03d}"

        self.chapter_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ----------------------------------------------------

    def _generate_chunks(self, chapter):

        """
        Genera todos los chunks.
        """

        total = len(chapter.chunks)

        for chunk in chapter.chunks:

            wav = self.chapter_dir / f"chunk_{chunk.number:03d}.wav"

            if wav.exists():

                utils.info(
                    f"[{chunk.number}/{total}] existente"
                )

                chunk.audio_file = str(wav)

                chunk.generated = True

                continue

            utils.info(
                f"[{chunk.number}/{total}] generando..."
            )

            subprocess.run(

                [

                    config.PIPER_BIN,

                    "--model",

                    config.VOICE_FILE,

                    "--output_file",

                    str(wav)

                ],

                input=chunk.text,

                text=True,

                check=True

            )

            chunk.audio_file = str(wav)

            chunk.generated = True

    # ----------------------------------------------------

    def _merge_chunks(self, chapter):

        """
        Une todos los WAV usando ffmpeg.
        """

        final = self.chapter_dir / "final.wav"

        if final.exists():

            return final

        concat = self.chapter_dir / "concat.txt"

        with concat.open("w", encoding="utf8") as f:

            for chunk in chapter.chunks:

                f.write(
                    f"file '{Path(chunk.audio_file).name}'\n"
                )

        subprocess.run(

            [

                config.FFMPEG_BIN,

                "-y",

                "-f",

                "concat",

                "-safe",

                "0",

                "-i",

                str(concat),

                "-c",

                "copy",

                str(final)

            ],

            cwd=self.chapter_dir,

            check=True,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL

        )

        return final

    # ----------------------------------------------------

    def _update(self, chapter, audio):

        """
        Actualiza el capítulo.
        """

        chapter.audio_file = str(audio)

        chapter.generated = True

        utils.ok(f"Capítulo {chapter.number} listo.")
