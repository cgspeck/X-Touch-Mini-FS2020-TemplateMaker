from pathlib import Path
from tkinter import CENTER, YES, filedialog as fd
from tkinter import messagebox
from typing import List, Optional, Union


from template_maker import vars


def noop():
    pass


def do_error_box(title: str, message: str):
    messagebox.showerror(title, message)


def select_aircraft_config(initial_dir: Union[str, Path]) -> Optional[Path]:
    filetypes = (("Aircraft Configs", "config*.json"), ("All files", "*.*"))

    if type(initial_dir) != str:
        _initial_dir = str(initial_dir)
    else:
        _initial_dir = initial_dir

    filename = fd.askopenfilename(
        title="Select aircraft config", initialdir=_initial_dir, filetypes=filetypes
    )

    if len(filename) == 0:
        return None

    return Path(filename)


def save_dialog(fileext: str, filetype_desc: str) -> Optional[Path]:
    filetypes = ((filetype_desc, f"*.{fileext}"), ("All files", "*.*"))

    filename = fd.asksaveasfilename(
        title="Save image",
        initialdir=vars.mydocs_path,
        filetypes=filetypes,
        defaultextension=fileext,
    )

    if len(filename) == 0:
        return None

    return Path(filename)
