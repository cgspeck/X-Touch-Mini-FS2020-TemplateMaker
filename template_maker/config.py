from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from template_maker.errors import PrerequsitesNotFoundException
from template_maker.logger import get_logger

SCHEMA_VERSION = 0
CONFIG_DIR = Path(Path.home(), "x-touch-mini-fs2020-template-maker")
CONFIG_FILE = Path(CONFIG_DIR, "config.json")

logger = get_logger()


@dataclass
class Config:
    inkscape_path: Path
    xtouch_mini_fs2020_path: Path
    schema_version = SCHEMA_VERSION

    @classmethod
    def locate_file(cls, filename) -> Optional[Path]:
        memo = None
        for root, dirs, files in os.walk("c:\\"):
            for file in files:
                if file == filename:
                    memo = Path(root, filename)
                    break
            if memo is not None:
                break

        if memo is None:
            logger.error(f"Unable to locate '{filename}'")

        return memo

    @classmethod
    def create(cls) -> Config:
        logger.info("Looking for Inkscape...")
        inkscape_path = cls.locate_file("inkscape.exe")
        logger.info("Looking for X-Touch-Mini-FS2020...")
        xtouch_mini_fs2020_path = cls.locate_file("X-Touch-Mini-FS2020.exe")
        if inkscape_path is None or xtouch_mini_fs2020_path is None:
            raise PrerequsitesNotFoundException()

        memo = cls(
            inkscape_path,
            xtouch_mini_fs2020_path
        )

        memo.save()
        return memo

    @classmethod
    def load(cls) -> Config:
        if CONFIG_FILE.exists():
            dct = json.loads(CONFIG_FILE.read_text())

            if 'schema_version' in dct:
                del(dct['schema_version'])
            dct['inkscape_path']: Path(dct['inkscape_path'])
            dct['xtouch_mini_fs2020_path']: Path(dct['xtouch_mini_fs2020_path'])
            return cls(**dct)

        return cls.create()

    def save(self):
        if not CONFIG_DIR.exists():
            logger.info(f"Creating directory '{CONFIG_DIR}'")
            CONFIG_DIR.mkdir()

        memo = {
            'inkscape_path': str(self.inkscape_path),
            'xtouch_mini_fs2020_path': str(self.xtouch_mini_fs2020_path),
            'schema_version': self.schema_version
        }
        logger.info(f"Writing '{CONFIG_FILE}'")
        CONFIG_FILE.write_text(json.dumps(memo))
