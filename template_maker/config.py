from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
from semver import VersionInfo

from template_maker.errors import PrerequsitesNotFoundException
from template_maker.logger import get_logger
from template_maker.vars import data_path

SCHEMA_VERSION = 1
CONFIG_FILE = Path(data_path, "config.json")

logger = get_logger()


@dataclass
class Config:
    inkscape_path: Path
    xtouch_mini_fs2020_path: Path
    remove_unrecognized: bool
    defaults_enabled: bool
    xtouch_mini_fs2020_aircraft_path: Path = field(init=False)
    default_mapping_version: VersionInfo
    schema_version = SCHEMA_VERSION

    def __post_init__(self):
        self.xtouch_mini_fs2020_aircraft_path = Path(
            self.xtouch_mini_fs2020_path, "Configurations"
        )

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
            raise PrerequsitesNotFoundException(
                inkscape_found=inkscape_path is not None,
                xtouch_fs2020_found=xtouch_mini_fs2020_path is not None,
            )

        memo = cls(
            inkscape_path=inkscape_path,
            xtouch_mini_fs2020_path=xtouch_mini_fs2020_path.parent,
            remove_unrecognized=True,
            defaults_enabled=True,
        )

        memo.save()
        return memo

    @classmethod
    def load(cls) -> Config:
        if CONFIG_FILE.exists():
            dct: Dict[str, Any] = json.loads(CONFIG_FILE.read_text())

            if "schema_version" in dct:
                del dct["schema_version"]
            dct["inkscape_path"] = Path(dct["inkscape_path"])
            dct["xtouch_mini_fs2020_path"] = Path(dct["xtouch_mini_fs2020_path"])
            dct["defaults_enabled"] = dct.get("defaults_enabled", True)
            return cls(**dct)

        return cls.create()

    def save(self):
        memo = {
            "defaults_enabled": self.defaults_enabled,
            "inkscape_path": str(self.inkscape_path),
            "remove_unrecognized": self.remove_unrecognized,
            "schema_version": self.schema_version,
            "xtouch_mini_fs2020_path": str(self.xtouch_mini_fs2020_path),
        }
        logger.info(f"Writing '{CONFIG_FILE}'")
        CONFIG_FILE.write_text(json.dumps(memo, sort_keys=True, indent=2))
