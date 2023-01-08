from queue import Queue
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import CENTER, YES, Event
from tkinter import messagebox, ttk
from typing import List, Optional, Union
from uuid import UUID, uuid4
import webbrowser

from PIL import Image, ImageTk
from win32api import GetSystemMetrics


from template_maker.config import Config
from template_maker.generator_thread import GeneratorThread
from template_maker.generator_util import PNG_DIM
from template_maker.gui.util import do_error_box, save_dialog, select_aircraft_config
from template_maker.gui.label_mapping_editor import LabelMappingEditor
from template_maker.logger import get_logger
from template_maker.message import Message, MessageType
from template_maker.template_info import TemplateInfo


from template_maker.text_mapping import (
    TextMapping,
    load_mappings,
    reset_mappings,
    save_mappings,
)
from template_maker.update_check_thread import UpdateCheckResult, UpdateCheckThread
from template_maker.utils import generate_mapping_templates
from template_maker.version import VERSION


logger = get_logger()

WIDGET_IMAGE_FRAME_NAME = "image_frame"
WIDGET_PROCESS_PROGRESSBAR_NAME = "processing_progressbar"

MENU_RELOAD_TEXT = "Reload (F5)"


class App(tk.Tk):
    def __init__(
        self,
        config: Config,
        queue: Queue,
        pending_generation_job_id: UUID,
    ):
        super().__init__()
        screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
        image_original_width, image_original_height = PNG_DIM[0], PNG_DIM[1]
        window_width, window_height = max(screen_width // 2, image_original_width), max(
            screen_height // 2, image_original_height
        )
        self.window_width = window_width
        self.window_height = window_height
        self.title(f"X-Touch Mini FS2020 Template Maker {VERSION}")
        self.geometry("{}x{}".format(window_width, window_height))

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(
            label="Open...", command=lambda: self.select_and_load(None)
        )
        self.filemenu.add_command(
            label=MENU_RELOAD_TEXT, command=self.reload, state="disabled"
        )
        self.filemenu.add_command(
            label="Save PNG...", command=self.save_png, state="disabled"
        )
        self.filemenu.add_command(
            label="Save SVG...", command=self.save_svg, state="disabled"
        )
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=False)
        self.editmenu.add_command(
            label="Manage label mappings...",
            command=self.show_label_mapping_editor,
        )
        self.editmenu.add_command(
            label="Restore default mappings",
            command=self.confirm_and_reset_mappings,
        )

        self.desired_blank_setting = tk.BooleanVar(
            self, value=config.remove_unrecognized
        )
        self.editmenu.add_checkbutton(
            label="Blank out unrecognized labels",
            command=self.update_blank_setting_and_reload,
            onvalue=True,
            offvalue=False,
            variable=self.desired_blank_setting,
        )
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=False)
        self.helpmenu.add_command(
            label="Check for updates...",
            command=self.check_for_update,
        )
        self.helpmenu.add_command(
            label="About",
            command=self.show_about_message,
        )
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.config(menu=self.menubar)
        self.resizable(False, False)

        self.loaded_image_file_path: Optional[Path] = None
        self.current_template_info: Optional[TemplateInfo] = None

        self._config = config
        self.queue = queue
        self.pending_generation_job_id: Optional[UUID] = pending_generation_job_id
        self.bind("<F5>", self.reload)
        self.show_progressbar()
        self.check_queue()

    def show_progressbar(self):
        if self.loaded_image_file_path is not None:
            self.nametowidget(f".{WIDGET_IMAGE_FRAME_NAME}").destroy()

        pb = ttk.Progressbar(
            self,
            mode="indeterminate",
            name=WIDGET_PROCESS_PROGRESSBAR_NAME,
            maximum=5,
        )
        pb.start()
        pb.place(relx=0.5, rely=0.5, anchor=CENTER)

    def check_for_update(self):
        job_id = uuid4()
        logger.info(f"Submitting update check job {job_id}")
        t = UpdateCheckThread(job_id, self.queue, logger, VERSION)
        t.start()

    def check_queue(self):
        if not self.queue.empty():
            msg: Message = self.queue.get_nowait()
            logger.info(f"Received message {msg}")

            if msg.message_type == MessageType.GENERATION_COMPLETE:
                if msg.job_id == self.pending_generation_job_id:
                    self.pending_generation_job_id = None
                    logger.info("Loading image...")
                    self.process_generation_complete_message(msg.get_template_info())
                else:
                    logger.info("Discarding unexpected message")
            if msg.message_type == MessageType.UPDATE_CHECK_COMPLETE:
                self.process_update_check_complete_message(
                    msg.get_update_check_result()
                )

        self.after(100, self.check_queue)

    def process_update_check_complete_message(
        self, update_check_result: UpdateCheckResult
    ):
        update_check_title = "Update Check"
        if (
            update_check_result.latest_version is None
            or update_check_result.error_message is not None
        ):
            msg = "Unable to do update check!"

            if update_check_result.error_message is not None:
                msg += f"\n\n{update_check_result.error_message}"

            messagebox.showerror(update_check_title, msg)
            return

        if update_check_result.update_available:
            msg = f"New version {update_check_result.latest_version} is available."
            latest_url = update_check_result.latest_url

            if latest_url is None:
                messagebox.showinfo(update_check_title, msg)
                return

            msg = f"{msg}\n\nWould you like to open a webpage to view and download the release?"
            yn = messagebox.askyesno(
                update_check_title,
                msg,
            )

            if yn == YES:
                webbrowser.open(latest_url)
            return

        messagebox.showinfo(update_check_title, "You have the latest version")

    def process_generation_complete_message(self, template_info: TemplateInfo):
        if len(template_info.error_msgs) > 0:
            msg = "\n".join(template_info.error_msgs)
            do_error_box("Error parsing aircraft config", msg)
        self.current_template_info = template_info

        if template_info.dest_png is None:
            return

        self.load_image(template_info.dest_png)
        self.check_for_unmapped_labels()

    def disable_template_loaded_menus(self):
        self.filemenu.entryconfig(MENU_RELOAD_TEXT, state="disabled")
        self.filemenu.entryconfig("Save PNG...", state="disabled")
        self.filemenu.entryconfig("Save SVG...", state="disabled")

    def enable_template_loaded_menus(self):
        self.filemenu.entryconfig(MENU_RELOAD_TEXT, state="normal")
        self.filemenu.entryconfig("Save PNG...", state="normal")
        self.filemenu.entryconfig("Save SVG...", state="normal")

    def reload(self, _event: Optional[Event] = None):
        if self.current_template_info is None:
            return

        self.select_and_load(self.current_template_info.filepath)

    def select_and_load(self, ac_config: Optional[Union[str, Path]]):
        if ac_config is None:
            ac_config = select_aircraft_config(
                self._config.xtouch_mini_fs2020_aircraft_path
            )

        if ac_config is None:
            return

        if not isinstance(ac_config, Path):
            ac_config = Path(ac_config)

        # generate the thing
        self.disable_template_loaded_menus()
        self.show_progressbar()
        job_id = uuid4()
        logger.info(f"Submitting generation job {job_id}")
        self.pending_generation_job_id = job_id
        t = GeneratorThread(
            job_id=job_id,
            queue=self.queue,
            logger=logger,
            config=self._config,
            ac_config=ac_config,
        )
        t.start()

    def check_for_unmapped_labels(self):
        if self.current_template_info is None:
            return

        unmapped_labels = self.current_template_info.gather_unmapped_labels()

        if len(unmapped_labels) == 0:
            return

        message = f"{len(unmapped_labels)} umapped labels were detected,\nwould you like to define them now?"
        choice = messagebox.askquestion(
            title="Unmapped labels detected",
            message=message,
        )

        if choice == "no":
            return

        self.show_label_mapping_editor(True)

    def show_label_mapping_editor(self, initially_filtered: bool = False):
        if self.current_template_info is None:
            return

        if self.check_for_unmapped_labels is not None:
            mappings = self.current_template_info.mappings
        else:
            mappings = load_mappings()

        mappings.extend(
            generate_mapping_templates(
                self.current_template_info.gather_unmapped_labels()
            )
        )
        mappings.sort()
        LabelMappingEditor(
            self,
            save_callback=self.save_mappings_and_reload,
            mappings=mappings,
            initially_filtered=initially_filtered,
        )

    def save_mappings_and_reload(self, updated_mappings: List[TextMapping]):
        selected: List[TextMapping] = []

        for m in updated_mappings:
            if m.modified or not m.new:
                selected.append(m)

        save_mappings(selected)
        self.reload()

    def confirm_and_reset_mappings(self):
        message = f"This will replace all custom mappings with the default. Are you sure you want to continue?"
        choice = messagebox.askquestion(
            title="Reset user mappings?",
            message=message,
        )

        if choice == "no":
            return

        reset_mappings()
        self.reload()

    def load_image(self, image_file_path: Path):
        self.nametowidget(f"{WIDGET_PROCESS_PROGRESSBAR_NAME}").destroy()

        img = Image.open(image_file_path)
        window_width = self.window_width
        window_height = self.window_height
        img.thumbnail((window_width, window_height), Image.Resampling.LANCZOS)
        self.python_image = ImageTk.PhotoImage(img)
        frame = ttk.Frame(
            self,
            width=window_width,
            height=window_height,
            name=WIDGET_IMAGE_FRAME_NAME,
        )
        frame.pack()
        label = ttk.Label(frame, image=self.python_image)
        label.pack(fill="both", expand=True)
        self.loaded_image_file_path = image_file_path
        self.enable_template_loaded_menus()

    def save_png(self):
        if (
            self.current_template_info is None
            or self.current_template_info.dest_png is None
        ):
            return

        fp = save_dialog("PNG files", "png")
        if fp is None:
            return

        if fp.suffix.lower() != ".png":
            fp = fp.parent / (fp.name + ".png")

        logger.info(f"Writing {fp}")
        shutil.copy(self.current_template_info.dest_png, fp)

    def save_svg(self):
        if (
            self.current_template_info is None
            or self.current_template_info.dest_svg is None
        ):
            return

        fp = save_dialog("SVG files", "svg")
        if fp is None:
            return

        if fp.suffix.lower() != ".svg":
            fp = fp.parent / (fp.name + ".svg")

        logger.info(f"Writing {fp}")
        shutil.copy(self.current_template_info.dest_svg, fp)

    def update_blank_setting_and_reload(self):
        self._config.remove_unrecognized = self.desired_blank_setting.get()
        self._config.save()
        self.reload()

    def show_about_message(self):
        msg = f"""X-Touch Mini FS2020 Template Maker {VERSION}

Copyright (C) 2023  Chris Speck

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
        """
        messagebox.showinfo(
            "About",
            msg,
        )
