from pathlib import Path
from semver import VersionInfo

VERSION = None
VERSION_FILE = Path("build_tag")
DEFAULT_VERSION = VersionInfo(0, 0, 0)


def version_from_file(p: Path):
    return VersionInfo.parse(p.read_text().strip("v"))


if VERSION is None:
    if VERSION_FILE.exists():
        VERSION = version_from_file(VERSION_FILE)
    else:
        VERSION = DEFAULT_VERSION
