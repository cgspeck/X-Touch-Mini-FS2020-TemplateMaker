from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
from typing import Optional, Union

def do_error_box(title: str, message: str):
    showerror(title, message)

def select_aircraft_config(initial_dir: Union[str, Path]) -> Optional[Path]:
    filetypes = (
        ('Aircraft Configs', 'config*.json'),
        ('All files', '*.*')
    )

    if type(initial_dir) != str:
        _initial_dir = str(initial_dir)
    else:
        _initial_dir = initial_dir

    filename = fd.askopenfilename(
        title='Select aircraft config',
        initialdir=_initial_dir,
        filetypes=filetypes)

    if len(filename) == 0:
        return None

    return Path(filename)
