"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-08 for version 1.0b1

Error window

"""

import tkinter as tk

class HelpWindow(tk.Toplevel):

    def __init__(self, errormessage):
        super().__init__(errormessage)

        # Widgets
        self.title("Error!")

        # Help label
        errorlabel = tk.Label(self, text=errormessage)
        errorlabel.grid(row=0, column=0, padx=5, pady=5)

        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=1, column=0, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)