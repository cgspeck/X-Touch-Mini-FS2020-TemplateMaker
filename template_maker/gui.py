import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showerror
from typing import Optional, Union

from PIL import Image, ImageTk
from win32api import GetSystemMetrics

from template_maker import aircraft_config, main
from template_maker.config import Config
from template_maker.logger import get_logger
from template_maker.text_mapping import load_mappings
from template_maker.vars import output_path

logger = get_logger()


def noop():
    pass


def make_preview_app(config: Config, image_file_path: Optional[Path]) -> tk.Tk:
    screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
    image_original_width, image_original_height = 0, 0

    if image_file_path:
        img = Image.open(image_file_path)
        image_original_width, image_original_height = img.width, img.height

    window_width, window_height = max(screen_width // 2, image_original_width), max(
        screen_height // 2, image_original_height
    )

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Template preview")
            self.geometry("{}x{}".format(window_width, window_height))

            menubar = tk.Menu(self)
            filemenu = tk.Menu(menubar, tearoff=False)
            filemenu.add_command(label="Open", command=self.select_and_load)
            filemenu.add_command(label="Exit", command=self.quit)
            menubar.add_cascade(label="File", menu=filemenu)
            self.config(menu=menubar)

            self.loaded_image_file_path: Optional[Path] = None

            self._config = config

            if image_file_path is not None:
                self.load_image(image_file_path)

        def select_and_load(self):
            ac_config = select_aircraft_config(
                self._config.xtouch_mini_fs2020_aircraft_path
            )

            if ac_config is None:
                return

            # generate the thing
            mappings = load_mappings(False)
            template_info = aircraft_config.parse_aircraft_config(ac_config)
            template_info.apply_template_mappings(mappings)

            if len(template_info.error_msgs) > 0:
                for m in template_info.error_msgs:
                    logger.error(m)

                msg = "\n".join(template_info.error_msgs)
                do_error_box("Error parsing aircraft config", msg)

            fn = f"{int(time.time())}"
            dest_svg = Path(output_path, f"{fn}.svg")
            dest_png = Path(output_path, f"{fn}.png")
            print("before")
            main.run_generator(template_info, dest_svg, dest_png)
            print("after")
            self.load_image(dest_png)

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
