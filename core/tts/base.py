"""
Motor base para todos los TTS.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from core.models import Chapter


class BaseTTSEngine(ABC):

    def __init__(self, output_dir: Path):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    @abstractmethod
    def generate(self, chapter: Chapter) -> Path:
        """
        Genera el audio del capítulo.

        Devuelve la ruta del archivo generado.
        """
        pass
