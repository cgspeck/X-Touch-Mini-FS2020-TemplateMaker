import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from typing import Optional, Union

from PIL import Image, ImageTk
from win32api import GetSystemMetrics

from template_maker import main
from template_maker.config import Config
from template_maker.generator import PNG_DIM
from template_maker.logger import get_logger
from template_maker.template_info import TemplateInfo

logger = get_logger()
GUI_MODE = True


def noop():
    pass


def make_preview_app(config: Config, template_info: TemplateInfo) -> tk.Tk:
    screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
    image_original_width, image_original_height = PNG_DIM[0], PNG_DIM[1]

    window_width, window_height = max(screen_width // 2, image_original_width), max(
        screen_height // 2, image_original_height
    )

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Template preview")
            self.geometry("{}x{}".format(window_width, window_height))

            self.menubar = tk.Menu(self)
            self.filemenu = tk.Menu(self.menubar, tearoff=False)
            self.filemenu.add_command(
                label="Open", command=lambda: self.select_and_load(None)
            )
            self.filemenu.add_command(
                label="Reload", command=self.reload, state="disabled"
            )
            self.filemenu.add_command(label="Exit", command=self.quit)

            self.menubar.add_cascade(label="File", menu=self.filemenu)
            self.config(menu=self.menubar)

            self.loaded_image_file_path: Optional[Path] = None
            self.current_template_info: Optional[TemplateInfo] = None

            self._config = config

            if template_info is not None:
                self.current_template_info = template_info
                self.load_image(template_info.dest_png)

        def reload(self):
            self.select_and_load(self.current_template_info.filepath)

        def select_and_load(self, ac_config: Optional[str]):
            if ac_config is None:
                ac_config = select_aircraft_config(
                    self._config.xtouch_mini_fs2020_aircraft_path
                )

            if ac_config is None:
                return

            # generate the thing
            template_info = main.load_mappings_and_run(
                logger, config, GUI_MODE, ac_config
            )
            self.current_template_info = template_info
            self.load_image(template_info.dest_png)

        def load_image(self, image_file_path: Path):
            if self.loaded_image_file_path is not None:
                self.nametowidget(".image_frame").destroy()

            img = Image.open(image_file_path)
            img.thumbnail([window_width, window_height], Image.Resampling.LANCZOS)
            self.python_image = ImageTk.PhotoImage(img)
            frame = tk.Frame(
                self, width=window_width, height=window_height, name="image_frame"
            )
            frame.pack()
            tk.Label(frame, image=self.python_image).pack(fill="both", expand=True)
            self.loaded_image_file_path = image_file_path
            self.filemenu.entryconfig("Reload", state="normal")

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
