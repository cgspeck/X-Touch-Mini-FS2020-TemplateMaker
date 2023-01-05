#! /usr/bin/env python3
from pathlib import Path
import shutil

FROM = Path("tests\data\expected_svg_happy_path.svg")
DEST_DIR = Path("scratch")
TO = Path(DEST_DIR, "config_generic_ap.svg")

if not DEST_DIR.exists():
    DEST_DIR.mkdir()

shutil.copy(FROM, TO)
