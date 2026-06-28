"""
utils.py

Funciones auxiliares para PDFVoice.
"""

from __future__ import annotations

import hashlib
import logging
import re
import shutil
import sys
import time

from pathlib import Path

import config


# ==========================================================
# COLORES ANSI
# ==========================================================

class Color:

    RESET = "\033[0m"

    RED = "\033[91m"

    GREEN = "\033[92m"

    YELLOW = "\033[93m"

    BLUE = "\033[94m"

    CYAN = "\033[96m"

    BOLD = "\033[1m"


# ==========================================================
# MENSAJES
# ==========================================================

def info(msg: str):

    print(f"{Color.BLUE}[INFO]{Color.RESET} {msg}")


def ok(msg: str):

    print(f"{Color.GREEN}[ OK ]{Color.RESET} {msg}")


def warn(msg: str):

    print(f"{Color.YELLOW}[WARN]{Color.RESET} {msg}")


def error(msg: str):

    print(f"{Color.RED}[ERROR]{Color.RESET} {msg}")

    sys.exit(1)


# ==========================================================
# DIRECTORIOS
# ==========================================================

def ensure_directories():

    """
    Crea automáticamente todos los directorios
    necesarios del proyecto.
    """

    for d in (

        config.ROOT_DIR,

        config.CACHE_DIR,

        config.VOICE_DIR,

        config.TEMP_DIR,

        config.LOG_DIR,

    ):

        d.mkdir(parents=True, exist_ok=True)


# ==========================================================
# HASH SHA256
# ==========================================================

def sha256(path: Path) -> str:

    """
    Calcula el hash SHA256 de un archivo.
    """

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(65536)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


# ==========================================================
# NOMBRE SEGURO
# ==========================================================

def safe_filename(text: str) -> str:

    """
    Convierte cualquier texto
    en un nombre válido de archivo.
    """

    text = text.strip()

    text = text.replace(" ", "_")

    text = re.sub(r"[^\w\-]", "", text)

    return text


# ==========================================================
# DEPENDENCIAS
# ==========================================================

def check_dependencies():

    """
    Comprueba programas necesarios.
    """

    missing = []

    if config.PIPER_BIN is None:
        missing.append("piper")

    if config.MPV_BIN is None:
        missing.append("mpv")

    if config.PDFTOTEXT_BIN is None:
        missing.append("pdftotext")

    if missing:

        error(
            "Faltan dependencias:\n\n"
            + "\n".join(f" • {x}" for x in missing)
        )
    if config.FFMPEG_BIN is None:
        missing.append("ffmpeg")

    ok("Dependencias verificadas.")


# ==========================================================
# LOGGING
# ==========================================================

def init_logger():

    logfile = config.LOG_DIR / "pdfvoice.log"

    logging.basicConfig(

        filename=logfile,

        level=logging.INFO,

        format="%(asctime)s %(levelname)s %(message)s"

    )

    logging.info("========== Inicio ==========")


# ==========================================================
# TEMPORIZADOR
# ==========================================================

class Timer:

    def __init__(self):

        self.start = None


    def __enter__(self):

        self.start = time.perf_counter()

        return self


    def __exit__(self, *args):

        elapsed = time.perf_counter() - self.start

        ok(f"Tiempo: {elapsed:.2f} segundos")
