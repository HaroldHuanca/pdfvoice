"""
config.py

Configuración global de PDFVoice.
"""

from pathlib import Path
import shutil

# ============================================================
# DIRECTORIOS
# ============================================================

HOME = Path.home()

ROOT_DIR = HOME / "PDFVoice"

CACHE_DIR = ROOT_DIR / "cache"

VOICE_DIR = ROOT_DIR / "voices"

TEMP_DIR = ROOT_DIR / "temp"

LOG_DIR = ROOT_DIR / "logs"

# ============================================================
# ARCHIVOS
# ============================================================

CONFIG_FILE = ROOT_DIR / "config.json"

LAST_SESSION_FILE = ROOT_DIR / "last_session.json"

# ============================================================
# PROGRAMAS EXTERNOS
# ============================================================

def find_piper():

    # Si está en el PATH
    p = shutil.which("piper")
    if p:
        return p

    # Rutas comunes
    posibles = [
        Path.home() / "Aplicaciones/piper/piper/piper",
        Path.home() / "Applications/piper/piper/piper",
        Path.home() / "piper/piper",
    ]

    for ruta in posibles:
        if ruta.exists() and ruta.is_file():
            return str(ruta)

    return None


PIPER_BIN = find_piper()

MPV_BIN = shutil.which("mpv")

PDFTOTEXT_BIN = shutil.which("pdftotext")

FFMPEG_BIN = shutil.which("ffmpeg")

MPV_SOCKET = "/tmp/pdfvoice.sock"
# ============================================================
# VOZ POR DEFECTO
# ============================================================

def find_voice():

    posibles = [

        Path.home() / "Aplicaciones/piper/piper/voices",

        ROOT_DIR / "voices",

    ]

    for carpeta in posibles:

        if carpeta.exists():

            voces = list(carpeta.glob("*.onnx"))

            if voces:
                return str(voces[0])

    return None


VOICE_FILE = find_voice()

DEFAULT_SPEED = 1.0

DEFAULT_LINES = 1500

# ============================================================
# PATRONES PARA DETECTAR CAPÍTULOS
# ============================================================

CHAPTER_PATTERNS = [

    r"^CAP[IÍ]TULO\s+\d+$",

    r"^Cap[ií]tulo\s+\d+$",

    r"^CAP[IÍ]TULO\s+[IVXLCDM]+$",

    r"^Cap[ií]tulo\s+[IVXLCDM]+$",

    r"^\d+\.\s+.+$",

    r"^\d+\s+.+$",

    r"^[IVXLCDM]+\.\s+.+$",

    r"^Introducci[oó]n$",

    r"^Marco Te[oó]rico$",

    r"^Metodolog[ií]a$",

    r"^Resultados$",

    r"^Discusi[oó]n$",

    r"^Conclusiones$",

    r"^Recomendaciones$",

    r"^Bibliograf[ií]a$",

    r"^Referencias$",

    r"^Anexos?$"

]
