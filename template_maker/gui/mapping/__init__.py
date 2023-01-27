from pathlib import Path
import shutil
import tkinter as tk
from typing import Callable, List, Optional
from tkinter import filedialog as fd
from tkinter import messagebox
from template_maker.config import Config

from template_maker.gui.util import save_dialog
from template_maker.logger import get_logger
from template_maker import vars
from template_maker import text_mapping

from semver import VersionInfo

from template_maker.template_info import TemplateInfo

logger = get_logger()

MAPPING_FILE_EXT = "yaml"
MAPPING_FILE_DESC = "Mapping Files"


def export_mappings(
    self: tk.Tk,
    template_info: Optional[TemplateInfo],
    default_version: VersionInfo,
):
    if template_info is None:
        return

    fp = save_dialog(MAPPING_FILE_EXT, MAPPING_FILE_DESC)
    if fp is None:
        return

    if fp.suffix.lower() != f".{MAPPING_FILE_EXT}":
        fp = fp.parent / (fp.name + f".{MAPPING_FILE_EXT}")

    logger.info(f"Writing {fp}")
    text_mapping.export_mappings(template_info.mappings, default_version, Path(fp))


def import_mappings(self: tk.Tk, config: Config, success_cb: Callable[[], None]):
    filetypes = ((MAPPING_FILE_DESC, f"*.{MAPPING_FILE_EXT}"), ("All files", "*.*"))

    filename = fd.askopenfilename(
        title="Select mapping file", initialdir=vars.mydocs_path, filetypes=filetypes
    )

    if len(filename) == 0:
        return None

    fp = Path(filename)
    error_msg: Optional[str] = None

    try:
        new_mapping_version = text_mapping.import_mappings(
            fp, vars.user_mappings, vars.default_mappings
        )
    except Exception as err:
        error_msg = f"Error parsing '{fp.name}':\n{err}"

    if error_msg is not None:
        messagebox.showerror("Unable to load mappings", error_msg)
        return

    msg = f"User and Default mappings have been loaded from {fp.name}"

    if new_mapping_version != config.default_mapping_version:
        config.default_mapping_version = new_mapping_version
        config.save()
        msg += f"\n\nNew default mapping version is {new_mapping_version}"

    messagebox.showinfo(
        "Successfully loaded mappings",
        msg,
    )
    success_cb()


def reset_mappings(self: tk.Tk, success_cb: Callable[[], None]):
    yn = messagebox.askyesno(
        "Reset mappings?",
        "Are you sure you want to reset mappings?\n\nThis will delete all user mappings and reset\ndefault mappings to v1.0.0?",
        **{"icon": messagebox.WARNING},
    )

    if yn != tk.YES:
        return

    logger.info(f"Deleting {vars.user_mappings}")
    vars.user_mappings.unlink()
    logger.info(f"Deleting {vars.default_mappings}")
    vars.default_mappings.unlink()
    logger.info("Running success_cb")
    success_cb()
