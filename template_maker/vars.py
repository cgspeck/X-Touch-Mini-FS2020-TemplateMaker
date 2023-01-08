import ctypes.wintypes
from pathlib import Path

font_family = "monospace"

mydocs_path = None

if mydocs_path is None:
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(
        None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf
    )
    mydocs_path = Path(buf.value)

data_path = Path(mydocs_path, "xtouch-template-maker")

if not data_path.exists():
    data_path.mkdir()

output_path = Path(data_path, "out")

if not output_path.exists():
    output_path.mkdir()

resources_path = None

if resources_path is None:
    resources_path = Path(__file__).parent.parent / "resources"

default_mappings = Path(resources_path, "mappings.default.txt")

user_mappings = Path(data_path, "mappings.local.txt")

if not user_mappings.exists():
    user_mappings.touch()
