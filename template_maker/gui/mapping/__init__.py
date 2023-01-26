from pathlib import Path
import shutil
import tkinter as tk
from typing import Callable, List, Optional
from tkinter import filedialog as fd
from tkinter import messagebox

from template_maker.gui.util import save_dialog
from template_maker.logger import get_logger
from template_maker import vars
from template_maker import text_mapping

logger = get_logger()

MAPPING_FILE_EXT = "mappings"
MAPPING_FILE_DESC = "Mapping Files"


def backup_mappings(self: tk.Tk):
    fp = save_dialog(MAPPING_FILE_EXT, MAPPING_FILE_DESC)
    if fp is None:
        return

    if fp.suffix.lower() != f".{MAPPING_FILE_EXT}":
        fp = fp.parent / (fp.name + f".{MAPPING_FILE_EXT}")

    logger.info(f"Writing {fp}")
    shutil.copy(vars.user_mappings, fp)


# def confirm_and_reset_mappings(self: tk.Tk, success_cb: Callable[[], None]):
#     message = f"This will replace all custom mappings with the default. Are you sure you want to continue?"
#     choice = messagebox.askquestion(
#         title="Reset user mappings?",
#         message=message,
#     )

#     if choice == "no":
#         return

#     text_mapping.reset_mappings()
#     success_cb()


def import_mappings(self: tk.Tk, success_cb: Callable[[], None]):
    filetypes = ((MAPPING_FILE_DESC, f"*.{MAPPING_FILE_EXT}"), ("All files", "*.*"))

    filename = fd.askopenfilename(
        title="Select mapping file", initialdir=vars.mydocs_path, filetypes=filetypes
    )

    if len(filename) == 0:
        return None

    fp = Path(filename)
    error_msg: Optional[str] = None
    memo: List[text_mapping.TextMapping] = []

    try:
        memo = text_mapping.parse_file(fp, is_default=False)
        if len(memo) == 0:
            error_msg = f"'{fp.name}' appears to be invalid.\nNo mappings were loaded."

    except Exception as err:
        error_msg = f"Error parsing '{fp.name}':\n{err}"

    if error_msg is not None:
        messagebox.showerror("Unable to load mappings", error_msg)
        return
    logger.info(f"Writing {vars.user_mappings}")
    shutil.copy(fp, vars.user_mappings)

    messagebox.showinfo(
        "Successfully loaded mappings",
        f"{len(memo)} mappings have been loaded from {fp.name}",
    )
    success_cb()
