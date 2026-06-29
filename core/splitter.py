"""
splitter.py

Divide el texto en capítulos.
"""

from __future__ import annotations

import re
from pathlib import Path

import config
import utils

from core.logger import get_logger

from core.models import Chapter

SPECIAL_SECTIONS = {

    "RESUMEN",
    "ABSTRACT",
    "INTRODUCCIÓN",
    "INTRODUCCION",
    "PRÓLOGO",
    "PROLOGO",
    "PREFACIO",
    "AGRADECIMIENTOS",
    "DEDICATORIA",
    "CONCLUSIONES",
    "RECOMENDACIONES",
    "REFERENCIAS",
    "BIBLIOGRAFÍA",
    "BIBLIOGRAFIA",
    "ANEXOS",

}

INDEX_SECTIONS = {

    "ÍNDICE",
    "INDICE",
    "CONTENIDO",
    "TABLE OF CONTENTS",

}

class ChapterSplitter:

    def __init__(self, text_file: str | Path):

        self.text_file = Path(text_file)

        self.lines = []

        self.chapters = []

        self.headers =[]


    def load(self):

        get_logger().info("Leyendo archivo de texto...")

        with self.text_file.open(
            encoding="utf-8",
            errors="ignore"
        ) as f:

            self.lines = [x.rstrip() for x in f]

        get_logger().ok(f"{len(self.lines)} líneas cargadas.")
        self.index_line = self.find_index()

    def score(self, line: str):
        """
        Devuelve una puntuación para una línea.
        """

        score = 0

        original = line
        line = line.strip()

        upper = line.upper()

        # ===========================
        # SECCIONES IMPORTANTES
        # ===========================

        if upper in SPECIAL_SECTIONS:
            score += 10

        # El índice nunca debe convertirse en capítulo
        if upper in INDEX_SECTIONS:
            return -100

        if not line:
            return 0

        # ==========================================================
        # REGLAS POSITIVAS
        # ==========================================================

        # Coincide con un patrón de capítulo
        for pattern in config.CHAPTER_PATTERNS:
            if re.match(pattern, line):
                score += 5
                break

        # Línea corta
        if len(line) < 60:
            score += 2

        # Todo en mayúsculas
        if line.isupper():
            score += 1

        # No termina en punto
        if not line.endswith("."):
            score += 1

        # Parece centrado (muchos espacios al inicio)
        if len(original) - len(original.lstrip()) > 10:
            score += 2

        # ==========================================================
        # REGLAS NEGATIVAS
        # ==========================================================

        # Demasiados números → probablemente una tabla
        if len(re.findall(r"\d+", line)) >= 3:
            score -= 5

        # Contiene montos de dinero
        if "S/" in line:
            score -= 5

        # Muchas columnas (espacios consecutivos)
        if re.search(r"\s{4,}", original):
            score -= 3

        # Demasiadas palabras
        if len(line.split()) > 10:
            score -= 5

        # Parece una fila de tabla (número + texto + número)
        if re.match(r"^\d+\s+\w+", line):
            score -= 3

        # Muchos símbolos
        if len(re.findall(r"[/%$€()-]", line)) >= 2:
            score -= 2

        return score

    def detect(self):
        """
        Detecta posibles capítulos.
        """

        get_logger().info("Buscando capítulos...")

        encontrados = 0

        for i, line in enumerate(self.lines):

            s = self.score(line)

            if s >= 8:

                encontrados += 1

                title = self.merge_title(i)

                self.headers.append((i,title))


        get_logger().ok(f"{encontrados} posibles capítulos encontrados.")

    def merge_title(self, index: int):
        """
        Une el encabezado con la siguiente línea si parece
        formar parte del título.
        """

        title = self.lines[index].strip()

        for offset in range(1, 4):

            if index + offset >= len(self.lines):
                break

            candidate = self.lines[index + offset].strip()

            if not candidate:
                continue

            # Si parece otro capítulo, detenerse
            if self.score(candidate) >= 8:
                break

            # Debe ser corto
            if len(candidate) > 80:
                break

            # Evitar líneas de tablas
            if len(candidate.split()) > 12:
                break

            # Evitar números de página
            if candidate.isdigit():
                continue

            return title + " - " + candidate

        return title

    def find_index(self):
        """
        Busca el índice del documento.
        """

        for i, line in enumerate(self.lines[:400]):

            upper = line.strip().upper()

            if upper in INDEX_SECTIONS:

                get_logger().ok(f"Índice encontrado en la línea {i}")

                return i

        return None

    def build(self):
        """
        Construye objetos Chapter a partir de los encabezados detectados.
        """

        get_logger().info("Construyendo capítulos...")

        self.chapters = []

        if not self.headers:

            get_logger().warn("No hay encabezados detectados.")

            return []

        for idx, (start, title) in enumerate(self.headers):

            if idx + 1 < len(self.headers):
                end = self.headers[idx + 1][0]
            else:
                end = len(self.lines)

            text = "\n".join(self.lines[start:end]).strip()

            chapter = Chapter(

                number=idx + 1,

                title=title,

                text=text,

                start_line=start,

                end_line=end,

            )

            self.chapters.append(chapter)

        get_logger().ok(f"{len(self.chapters)} capítulos construidos.")

        return self.chapters

    def summary(self):
        """helo"""
