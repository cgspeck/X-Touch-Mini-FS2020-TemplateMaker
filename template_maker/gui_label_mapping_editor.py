import tkinter as tk


class LabelMappingEditor(tk.Toplevel):
    def __init__(self, parent, save_callback) -> None:
        super().__init__(parent)
        self.save_callback = save_callback
        # self = tk.Toplevel(self.root)
        self.geometry("800x800")
        self.title("Label Mapping Editor")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=0)
        tk.Listbox(self).grid(row=0, column=0)
        tk.Label(self, text="Foo").grid(row=0, column=1)
        button_frame = tk.Frame(self)
        tk.Button(button_frame, text="Cancel", command=self.cancel).grid(
            row=0, column=0
        )
        tk.Button(
            button_frame, text="Save & Close", command=self.do_save_callback
        ).grid(row=0, column=1)
        button_frame.grid(row=1, column=0, columnspan=2)
        self.grab_set()

    def cancel(self):
        self.destroy()

    def do_save_callback(self):
        self.save_callback()
        self.destroy()
