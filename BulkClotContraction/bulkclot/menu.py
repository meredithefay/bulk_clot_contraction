"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-08 for version 1.0b1

Main menu script directs to analysis GUI, help documentation

"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from PIL import Image, ImageTk
from bulkclot import gui, help
import sys
import os

class MainMenu(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # App details, subject to change
        name = 'Bulk clot contraction'
        tagline = 'Automated analysis software\nfor analysis of bulk clot contraction assay images'
        version = 'v0.1.0'

        # Fonts
        titlefont = font.Font(size=24)
        smallfont = font.Font(size=8)

        # Widgets
        self.title("Main menu")
        # Software name, title
        app_label = tk.Label(self, text=name)
        app_label['font'] = titlefont
        app_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        # Logo image
        logo_canvas = tk.Canvas(self, width=100, height=60)
        logo_canvas.grid(row=1, column=0, columnspan=3)
        new_path = self.resource_path('Logo.png')
        logoimg = Image.open(new_path)
        logoimg = ImageTk.PhotoImage(image=logoimg)  # A fix to keep image displayed
        self.logoimg = logoimg  # " "
        logo_canvas.create_image(0, 0, anchor='nw', image=logoimg)
        # Program description text
        desc_label = tk.Label(self, text=tagline)
        desc_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Start analysis button
        start_button = tk.Button(self, text="Start analysis", command=self.opengui)
        start_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        # Help button
        help_button = tk.Button(self, text="Help", command=self.openhelp)
        help_button.grid(row=4, column=0, padx=5, pady=5)
        # Version, Lam lab text
        lamlab_label = tk.Label(self, text=version +", Lam Lab")
        lamlab_label['font'] = smallfont
        lamlab_label.grid(row=4, column=1, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=4, column=2, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def opengui(self):
        gui.GUIWindow()

    def openhelp(self):
        help.HelpWindow()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, needed to display logo in .app"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


root = MainMenu()
root.mainloop()