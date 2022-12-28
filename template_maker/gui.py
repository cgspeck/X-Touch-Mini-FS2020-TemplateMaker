from pathlib import Path
from win32api import GetSystemMetrics
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from typing import Optional, Union

from PIL import Image


def make_preview_app(image_file_path: Path) -> tk.Tk:
    screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
    img = Image.open(image_file_path)
    image_original_width, image_original_height = img.width, img.height
    window_width, window_height = min(screen_width // 2, image_original_width), min(screen_height // 2, image_original_height)

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Template preview")
            self.geometry("{}x{}".format(window_width, window_height))
            img = Image.open(image_file_path)
            max_height = img.height
            img.thumbnail([window_width, max_height], Image.Resampling.LANCZOS)
            self.python_image = tk.PhotoImage(file=image_file_path)
            tk.Label(self, image=self.python_image).pack(fill="both", expand=True)

    return App


def do_error_box(title: str, message: str):
    showerror(title, message)


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
