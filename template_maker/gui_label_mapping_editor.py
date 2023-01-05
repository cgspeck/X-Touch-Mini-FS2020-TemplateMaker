import re
import tkinter as tk
from tkinter import Event, Toplevel, ttk
from tkinter import messagebox
from typing import Callable, List

from template_maker.text_mapping import TextMapping, sanitise_replacement

ITEM_TREEVIEW_NAME = "item-treeview"


class LabelMappingEditor(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        save_callback: Callable[[List[TextMapping]], None],
        mappings: List[TextMapping],
        initially_filtered: bool,
    ) -> None:
        super().__init__(parent)
        self.save_callback = save_callback
        self.geometry("800x800")
        self.title("Label Mapping Editor")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=0)

        self.desired_filter_setting = tk.BooleanVar(self, value=initially_filtered)
        # button_and_treeview_frame = ttk.Frame(self)
        cb = ttk.Checkbutton(
            self,
            text="Hide inactive mappings",
            onvalue=True,
            offvalue=False,
            variable=self.desired_filter_setting,
            command=self.show_entries,
        )
        cb.grid(row=0, column=0, sticky="nsew", columnspan=2)

        columns = ("pattern", "replacement", "in_use")
        tree = ttk.Treeview(
            self, columns=columns, show="headings", name=ITEM_TREEVIEW_NAME
        )
        tree.heading("pattern", text="Pattern")
        tree.heading("replacement", text="Replacement")
        tree.heading("in_use", text="In Use?")

        self.mappings = mappings

        # from https://stackoverflow.com/a/41991207
        # tree.bind("<Double-Button-1>", self.on_item_doubleclick)
        tree.bind("<Double-1>", self.on_item_doubleclick)
        tree.grid(row=1, column=0, sticky="nsew", columnspan=2)

        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).grid(
            row=0, column=0
        )
        ttk.Button(
            button_frame, text="Save & Close", command=self.do_save_callback
        ).grid(row=0, column=1)
        button_frame.grid(row=2, column=0, columnspan=2)
        self.show_entries()
        self.resizable(False, False)
        self.grab_set()

    def show_entries(self):
        filtered = self.desired_filter_setting.get()
        tree: ttk.Treeview = self.nametowidget(f"{ITEM_TREEVIEW_NAME}")

        for item in tree.get_children():
            tree.delete(item)

        for i, m in enumerate(self.mappings):
            if filtered and not m.in_use:
                continue

            tree.insert(
                "",
                tk.END,
                values=(m.pat.pattern, m.replacement_unsanitized, m.in_use),
                iid=f"iid-{i}",
            )

    def cancel(self):
        self.destroy()

    def do_save_callback(self):
        self.save_callback(self.mappings)
        self.destroy()

    def delete_current_entry(self, treeView):
        curr = treeView.focus()

        if "" == curr:
            return

        treeView.delete(curr)

    def validate_update(
        self,
        treeview: ttk.Treeview,
        pattern: str,
        replacement: str,
        in_use: bool,
        treeview_index: int,
        item_id: str,
    ):

        try:
            re_pat = re.compile(pattern)
        except:
            messagebox.showerror(
                "Update failed", f"Unable to update entry, invalid pattern '{pattern}'"
            )
            return False

        # update mappings!
        mapping_index = int(item_id.split("-")[1])
        self.mappings[mapping_index].pat = re_pat
        self.mappings[mapping_index].replacement = sanitise_replacement(replacement)
        self.mappings[mapping_index].replacement_unsanitized = replacement
        self.mappings[mapping_index].modified = True

        treeview.delete(item_id)

        # Put it back in with the updated values
        treeview.insert(
            "", treeview_index, values=(pattern, replacement, in_use), iid=item_id
        )

        return True

    def on_item_doubleclick(self, event: Event):
        # from https://stackoverflow.com/a/41991207
        treeView: ttk.Treeview = event.widget
        current_index = treeView.index(treeView.focus())
        # First check if a blank space was selected
        entry_id = treeView.focus()
        if "" == entry_id:
            return

        # Set up window
        win = Toplevel(self)
        win.title("Edit Entry")
        win.attributes("-toolwindow", True)
        win.resizable(False, False)

        ####
        # Set up the window's other attributes and geometry
        ####

        # Grab the entry's values
        for child in treeView.get_children():
            if child == entry_id:
                values = treeView.item(child)["values"]
                break

        col1Lbl = ttk.Label(win, text="Regex Search Pattern: ")
        col1Ent = ttk.Entry(win)
        col1Ent.insert(0, values[0])  # Default is column 1's current value
        col1Lbl.grid(row=0, column=0)
        col1Ent.grid(row=0, column=1)

        col2Lbl = ttk.Label(win, text="Replacement: ")
        col2Ent = ttk.Entry(win)
        col2Ent.insert(0, values[1])  # Default is column 2's current value
        col2Lbl.grid(row=0, column=2)
        col2Ent.grid(row=0, column=3)

        def update_then_destroy():
            if self.validate_update(
                treeView,
                col1Ent.get(),
                col2Ent.get(),
                values[2],
                current_index,
                entry_id,
            ):
                win.destroy()

        okButt = ttk.Button(win, text="Ok")
        okButt.bind("<Button-1>", lambda e: update_then_destroy())
        okButt.grid(row=1, column=4)

        canButt = ttk.Button(win, text="Cancel")
        canButt.bind("<Button-1>", lambda c: win.destroy())
        canButt.grid(row=1, column=5)
