#!/usr/bin/env python
from decimal import Decimal
import decimal
import locale as lc
import math

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # python 2
    import Tkinter as tk
    import ttk


# List theme names:

from pyrotocanvas.rcproject import RCProject

class ProjectFrame(ttk.Frame):
    def __init__(self, parent):
        self.localeResult = lc.setlocale(lc.LC_ALL, "")
        if self.localeResult == "C":
            lc.setlocale(lc.LC_ALL, "en_US")
        # example: moneyStr = lc.currency(amount, grouping=True)
        self.parent = parent
        root = self.parent
        self.seqPath = tk.StringVar()
        self.result = tk.StringVar()

        ttk.Frame.__init__(self, parent)
        self.menu = tk.Menu(parent)
        self.fileMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.fileMenu)

        self.fileMenu.add_command(label="Open", command=self.open)
        self.fileMenu.add_command(label="Save", command=self.save)
        self.fileMenu.add_command(label="Exit",
                                  command=self.parent.destroy)

        # self.themeMenu = tk.Menu(self.menu, tearoff=0)
        # self.menu.add_cascade(label="Theme", menu=self.themeMenu)
        # root.style = ttk.Style()
        # for name in root.style.theme_names():
        #     self.themeMenu.add_command(
        #         label=name,
        #         command=lambda: self.setTheme(name)
        #     )
        # ^ skip this. On Windows it is automatic, and on GNU+Linux
        #   systems, all of them (clam, alt, default, classic) are all
        #   the same, like old xwindows (thick "3D" edges like Windows
        #   3.1)

        parent.config(menu=self.menu)
        self.pack(fill=tk.BOTH, expand=True)
        row = 0
        ttk.Label(self, text="Sequence:").grid(column=0, row=row,
                                               sticky=tk.E)
        ttk.Entry(self, textvariable=self.seqPath).grid(column=1,
                                                        columnspan=3,
                                                        row=row,
                                                        sticky=tk.W)
        # Entry width=25, state="readonly"
        row += 1
        self.prev_button = ttk.Button(self, text="<", command=self.prev)
        self.prev_button.grid(column=0, row=row, sticky=tk.W)
        self.play_button = ttk.Button(self, text="Play",
                                      command=self.play)
        self.play_button.grid(column=1, row=row, sticky=tk.E)
        self.next_button = ttk.Button(self, text=">", command=self.next)
        self.next_button.grid(column=2, row=row, sticky=tk.E)
        row += 1
        # exitBtn = ttk.Button(self, text="Exit", command=root.destroy)
        # exitBtn.grid(column=2, row=row, sticky=tk.W)
        # row += 1

        self.canvas = tk.Canvas(self)
        self.canvas.grid(
            column=0,
            row=row,
            sticky=tk.W+tk.E,
            columnspan=3
        )
        row += 1

        # ttk.Label(self, text="Status: ").grid(column=0, row=row, sticky=tk.E)
        resultE = ttk.Entry(self, textvariable=self.result,
                            state="readonly")
        resultE.grid(column=0, columnspan=4, row=row, sticky=tk.E+tk.W)
        # grid sticky=tk.W
        row += 1

        for child in self.winfo_children():
            child.grid_configure(padx=6, pady=3)
        # self.prev_button['state'] = tk.DISABLED
        # self.next_button['state'] = tk.DISABLED

        self.project = RCProject()
        self.titleFmt = "RotoCanvas - {}"
        root.title(self.titleFmt.format(self.project.path))

    def setTheme(self, name):
        self.parent.style.theme_use(name)

    def next(self):
        pass

    def prev(self):
        pass

    def play(self):
        pass

    def save(self):
        saveError = self.project.save()
        if saveError is not None:
            self.result.set(saveError)

    def open(self):

        pass

    def end(self):
        pass


def main():
    root = tk.Tk()
    root.title("RotoCanvas")
    frame = ProjectFrame(root)
    project = frame.project
    root.mainloop()
    project.stop()
    saveError = project.save()
    if saveError is None:
        print("Save completed.")
    else:
        print("[pyrotocanvas run.py main] Save failed: {}"
              "".format(saveError))


if __name__ == "__main__":
    main()
