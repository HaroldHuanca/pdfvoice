"""
extractor.py

Extrae texto desde un PDF utilizando pdftotext.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import config
import utils


class PDFExtractor:
    """
    Convierte un PDF en texto plano utilizando pdftotext.
    """

    def __init__(self, pdf: str | Path):

        self.pdf = Path(pdf).expanduser().resolve()

        if not self.pdf.exists():
            raise FileNotFoundError(f"No existe el archivo:\n{self.pdf}")

    @property
    def output_dir(self) -> Path:
        """
        Directorio de trabajo asociado a este PDF.
        """

        pdf_hash = utils.sha256(self.pdf)

        directory = config.CACHE_DIR / pdf_hash

        directory.mkdir(parents=True, exist_ok=True)

        return directory

    @property
    def text_file(self) -> Path:
        """
        Archivo de texto generado.
        """

        return self.output_dir / "texto.txt"

    def extract(self, force: bool = False) -> Path:
        """
        Extrae el texto del PDF.

        Si ya existe el archivo de texto y force=False,
        reutiliza la caché.
        """

        if self.text_file.exists() and not force:

            utils.info("Usando texto en caché.")

            return self.text_file

        utils.info("Extrayendo texto del PDF...")

        command = [

            config.PDFTOTEXT_BIN,

            "-layout",

            str(self.pdf),

            str(self.text_file)

        ]

        try:

            subprocess.run(

                command,

                check=True,

                stdout=subprocess.DEVNULL,

                stderr=subprocess.PIPE,

                text=True

            )

        except subprocess.CalledProcessError as e:

            utils.error(e.stderr)

        utils.ok("Texto extraído correctamente.")

        return self.text_file

    def preview(self, lines: int = 20):
        """
        Muestra las primeras líneas del texto.
        """

        if not self.text_file.exists():

            utils.warn("Primero debes ejecutar extract().")

            return

        print()

        with self.text_file.open(
            encoding="utf-8",
            errors="ignore"
        ) as f:

            for i, line in enumerate(f):

                if i >= lines:
                    break

                print(line.rstrip())

        print()
