"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-08 for version 1.0b1

Help window

Bulk clot contraction help script directs provides information on
--User interface inputs, parameters, outputs for GUI
--Software author contact

"""

import tkinter as tk
import tkinter.scrolledtext as st

class HelpWindow(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # Widgets
        self.title("Help")

        # Help label
        helptitle = tk.Label(self, text="Bulk clot contraction help")
        helptitle.grid(row=0, column=0, padx=5, pady=5)
        # Text box
        helptext = st.ScrolledText(self,
                                   width=100,
                                   height=20,
                                   font=("Arial",
                                         10))
        helptext.grid(row=1, column=0, pady=10, padx=10)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=2, column=0, padx=5, pady=5)

        # Inserting Text which is read only
        helptext.insert(tk.INSERT,
        u"""\
        This bulk clot contraction assay analysis software is a free software developed by the Lam lab
        
        Bulk clot contraction analysis GUI analyzes images of bulk clots:

        Inputs:
        --A folder of images (.png, .jpg, .tif), chosen via button/file dialog
        ----Images should represent a time series
        ------Time will be given as image n, user must translate this to time based on image interval
        ----Images within the folder will be sorted alphabetically
        ------If greater than 9 images are used, label _01..., _09, _10 etc. to preserve order
        --Number of replicates per image - for example, if you have three cuvettes, n = 3
        --Reference square size
        ----Each image must have a reference square - reference square size should be given in mm2
        
        Steps:
        --Upon clicking button "run analysis"
        ----Each image will be showed sequentially
        ------First prompt: rotate image, all regions of interest (ROI) are chose as squares
        ------Second prompt: choose reference square
        ------Third through 3+2*n replicates prompts: rotate, choose an ROI, each clot
        --After all ROIs have been chosen, graph window will appear
        ------Area over time (top), volume over time (button)
        --Results are automatically exported
        
        Outputs:
        
        --Files are output in one subfolder in the folder of the images you chose

        --Numerical data (.xlsx):
        ----For each image (one sheet/timepoint-image):
        ------Area of clot in mm\u00b2 for each replicate
        ------Volume of clot in mm\u00b3, assumes isometric contraction for each replicate
        ----Summary sheet providing mean, standard deviation volume at each timepoint

        --Graphical data for series (.png):
        ----Area over time (line graph)
        ----Volume over time (line graph)

        --This software is presented as a beta version and as such is under continuous development
        ----Future improvements include labeled image outputs and a non-sequential analysis GUI window

        """)

        # Making the text read only
        helptext.configure(state='disabled')

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)