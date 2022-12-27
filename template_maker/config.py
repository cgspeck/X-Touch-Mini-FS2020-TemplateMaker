from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from template_maker.logger import get_logger

SCHEMA_VERSION = 0
CONFIG_DIR = Path(Path.home, "x-touch-mini-fs2020-template-maker")
CONFIG_FILE = Path(CONFIG_DIR, "config.json")

logger = get_logger()


@dataclass
class Config:
    inkscape_path: Path
    xtouch_mini_fs2020: Path

    @classmethod
    def locate_file(cls, filename) -> Optional[Path]:
        memo = list(Path().rglob(filename))
        if len(memo) == 0:
            logger.error(f"Unable to locate '{filename}'")
            return None

        return memo[0]

    @classmethod
    def create(cls) -> Config:
        inkscape_path = cls.locate_file(inkscape_path)

        pass

    def load() -> Config:
        return Config(inkscape_path=Path(""), xtouch_mini_fs2020=Path(""))

    def save(self):
        pass
