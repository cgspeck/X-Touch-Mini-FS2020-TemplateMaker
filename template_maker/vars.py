import ctypes.wintypes
from pathlib import Path

font_family = "monospace"

mydocs_path = None

if mydocs_path is None:
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    mydocs_path = Path(buf.value)

data_path = Path(mydocs_path, 'xtouch-template-maker')
output_path = Path(data_path, 'out')
