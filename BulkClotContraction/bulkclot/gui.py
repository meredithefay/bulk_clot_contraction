"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-14 for version 1.0b1

Main GUI script

See help file for an explanation of inputs, parameters, code function, and outputs

"""

import tkinter as tk
from tkinter import filedialog
import tkinter.font as font
import os
import glob
import cv2
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import bulkclot.rotategui as rg
import math
import matplotlib.pyplot as plt
import datetime
from tkinter import messagebox


class GUIWindow(tk.Toplevel):

    def __init__(self):
        super().__init__()

        # Fonts
        boldfont = font.Font(weight='bold')

        # Tkinter variables
        self.refsize = tk.DoubleVar(value=1)  # Reference square size in mm2, default 1
        self.ntp = tk.IntVar(value=1)  # Number of images/timepoints
        self.rep = tk.IntVar(value=1)  # Number of replicates per image
        self.dirname = tk.DoubleVar()

        # Widgets
        self.title("Bulk clot contraction analysis")

        # Input label
        input_label = tk.Label(self, text="Inputs")
        input_label['font'] = boldfont
        input_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        # Input directory button
        dir_button = tk.Button(self, text="Select folder of images", command=self.dirfile)
        dir_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='W')
        # Selected directory file name label
        self.dir_label = tk.Label(self, text="")
        self.dir_label.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        # Reference size label
        ref_label = tk.Label(self, text="Reference square size")
        ref_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='W')
        # Reference entry box
        ref_entry = tk.Entry(self, textvariable=self.refsize, width=20)
        ref_entry.grid(row=2, column=1, padx=5, pady=5)
        # mm2 entry box label
        mm_label = tk.Label(self, text=u"mm\u00b2")
        mm_label.grid(row=2, column=2, padx=5, pady=5, sticky='W')
        # Number replicates label
        rep_label = tk.Label(self, text="Number of replicates/image")
        rep_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='W')
        # Reference entry box
        ref_entry = tk.Entry(self, textvariable=self.rep, width=20)
        ref_entry.grid(row=3, column=1, columnspan=2,padx=5, pady=5)
        # Images label
        imgs_label = tk.Label(self, text="Selected images")
        imgs_label['font'] = boldfont
        imgs_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        # Auto-update image name label
        self.cur_label = tk.Label(self, text="")
        self.cur_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        # Canvas with images
        self.img_canvas = tk.Canvas(self, width=250, height=250)
        self.img_canvas.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        # Scale
        self.img_scale = tk.Scale(self, orient='horizontal', from_=1, to=self.ntp.get(),
                                 command=self.managescale)  # Default end value 1, will update when video chosen
        self.img_scale.grid_forget()
        # Run analysis button
        analysis_button = tk.Button(self, text="Run analysis with selected images", command=self.runanalysis)
        analysis_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        # Quit button
        quit_button = tk.Button(self, text="Quit", command=self.on_closing)
        quit_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky='E')

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    # Functions

    # Resize images to fit canvas
    def displayimg(self):
        """Display current image and image name, incl. resize images to fit canvas, maintaining aspect ratio"""

        cur_img_name = os.path.basename(filelist[self.img_scale.get()-1]).split(".")[0]
        self.cur_label.config(text=cur_img_name)

        cur_img = Image.open(filelist[self.img_scale.get()-1])
        width, height = cur_img.size
        # Resize to fit canvas, maintaining aspect ratio
        factor = 250 / np.max((width, height))
        dim = (int(height * factor), int(width * factor))
        cur_img_r = cur_img.resize(dim, Image.ANTIALIAS)


        # Add image to canvas
        cur_img_r = ImageTk.PhotoImage(image=cur_img_r)  # A fix to keep image displayed
        self.cur_img_r = cur_img_r  # " "
        self.img_canvas.create_image(125, 125, anchor='c', image=cur_img_r)

    # Choose folder of images, return sorted list
    def dirfile(self):
        """Return a sorted list of all image files (.png, .jpg, .tif) in a directory, configure GUI window"""

        global filelist

        inputdirectory = filedialog.askdirectory()  # Select directory
        os.chdir(inputdirectory)

        # Create a list of files (global variable)
        filelist_png = glob.glob(inputdirectory + '/*.png')
        filelist_jpg = glob.glob(inputdirectory + '/*.jpg')
        filelist_tif = glob.glob(inputdirectory + '/*.tif')
        filelist = sorted(filelist_png + filelist_jpg + filelist_tif)

        # Display folder name
        dirname = os.path.basename(inputdirectory)
        self.dirname.set(dirname)
        self.dir_label.config(text=dirname)

        # Create and change directory to a results file
        now = datetime.datetime.now()
        # Create timestamped results directory
        current_dir = os.getcwd()  # Select filepath

        output_folder = os.path.join(current_dir, 'Results, ' + now.strftime("%m_%d_%Y, %H_%M_%S"))
        os.mkdir(output_folder)
        os.chdir(output_folder)

        # Configure scale
        self.ntp.set(len(filelist))
        self.img_scale['to'] = self.ntp.get()
        self.img_scale.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.displayimg()

    def managescale(self, event):
        """Display image within series depending on scale"""

        self.displayimg()

    def rotateimage(self, mat, angle):
        """
        Rotates an image (angle in degrees) and expands image to avoid cropping
        """

        height, width = mat.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rmat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

        return rmat

    def runanalysis(self):
        """Start a sequential series of windows for each image provided

        Create dataframe (col: ref 1, col: rep 0...n, rows: each image)

        For each image in series:
        Step 1: rotate image to choose a reference ROI
        Step 2: choose reference ROI
        For each replicate:
        Step 3: rotate image to choose a clot ROI
        Step 4: choose a clot ROI"""


        results = {}  # Dictionary
        colnames = []  # Column names dataframe
        for i in range(self.ntp.get()):

            key = i
            imgname = os.path.basename(filelist[i]).split('.')[0]
            colnames.append(imgname)
            results[i] = []
            img = cv2.imread(filelist[i], 0)  # Read as greyscale

            # Run for reference
            # Rotate image
            r = rg.RotateGUI(imgname, img, 'reference', 'red')
            angle = r.submit()

            # Call function
            rmat = self.rotateimage(img, angle)
            # rmat_double = cv2.resize(rmat, (rmat.shape[1] * 2, rmat.shape[0] * 2), interpolation = cv2.INTER_AREA)

            # Choose ROI, save values
            fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
            roi = cv2.selectROI("Select ROI for reference square, press enter", rmat,
                                fromCenter)  # Choose ROI function from cv2 - opens a window to choose
            cv2.destroyAllWindows()  # Destroy window when ready - requires any keyboard inpit
            roi_crop = rmat[int(roi[1]):int(roi[1] + roi[3]),
                       int(roi[0]):int(roi[0] + roi[2])]  # Create cropped image
            cv2.imshow("Region of interest confirmation", roi_crop)  # Display image
            cv2.waitKey(0)  # Hold until user presses some key (done at every step)
            cv2.destroyAllWindows()  # Destroy windows when done (done at every step)

            # calculate value
            area = roi[3] * roi[2] # / 2 / 2  # Area = width * height, resized 2x

            # Update key
            results[key].append(area)

            for j in range(self.rep.get()):

                # Rotate image
                r = rg.RotateGUI(imgname, img, 'replicate ' + str(j+1), 'blue')
                angle = r.submit()

                # Call function
                rmat = self.rotateimage(img, angle)

                # Choose ROI, save values
                fromCenter = False  # Set up to choose as a drag-able rectangle rather than a rectangle chosen from center
                roi = cv2.selectROI("Select ROI for replicate " + str(j+1) + ", press enter", rmat,
                                        fromCenter)  # Choose ROI function from cv2 - opens a window to choose
                cv2.destroyAllWindows()  # Destroy window when ready - requires any keyboard inpit
                roi_crop = rmat[int(roi[1]):int(roi[1] + roi[3]),
                           int(roi[0]):int(roi[0] + roi[2])]  # Create cropped image
                cv2.imshow("Region of interest confirmation", roi_crop)  # Display image
                cv2.waitKey(0)  # Hold until user presses some key (done at every step)
                cv2.destroyAllWindows()  # Destroy windows when done (done at every step)

                # calculate value
                area = roi[3] * roi[2]  # Area = width * height

                # Update key
                results[key].append(area)

        # Create dataframe out of dictionary to save results

        cols = pd.DataFrame(colnames)

        df = pd.DataFrame.from_dict(results, orient='index')
        df_holder = pd.DataFrame(index=range(len(df)), columns=range(self.rep.get()))
        df = pd.concat([cols, df, df_holder], axis=1, ignore_index=True)

        columnlist = ['image', 'reference (pix)']
        for i in range(self.rep.get()):
            columnlist.append('area (mm\u00b2), replicate ' + str(i + 1))
        for i in range(self.rep.get()):
            columnlist.append('volume (\u03bcL), replicate ' + str(i + 1))

        df.columns = columnlist

        # Convert to area
        for i in range(len(df)):  # For each row/timepoint
            for j in range(self.rep.get()):  # For each replicate
                df.iloc[i, j + 2] = df.iloc[i, j + 2] / df.iloc[i, 1] * self.refsize.get()

        # Calculate volume
        for i in range(len(df)):  # For each row/timepoint
            for j in range(self.rep.get()):  # For each replicate
                df.iloc[i, 2 + self.rep.get() + j] = df.iloc[i, 2 + j] * math.sqrt(df.iloc[i, 2 + j])

        # Add mean area
        df['mean area (mm\u00b2)'] = df.iloc[:, 2:2 + self.rep.get()].mean(axis=1)
        # Add mean volume
        df['mean volume (\u03bcL)'] = df.iloc[:, 2 + self.rep.get():2 + self.rep.get() + self.rep.get()].mean(axis=1)

        # Create an area line graph
        areagraph = plt.figure()
        x = range(len(df))
        plt.title('Area')
        plt.ylabel('area (\u03bcm\u00b2)')
        plt.xlabel('time point (n)')
        for i in range(self.rep.get()):
            plt.plot(x, df.iloc[:, 2 + i], color='salmon')
        plt.plot(x, df.iloc[:, 2 + self.rep.get() + self.rep.get()], color='red')
        plt.savefig('bulkclot_area.png', dpi=300)

        # Make a volume graph
        volgraph = plt.figure()
        plt.title('Volume')
        plt.ylabel('volume (\u03bcm\u00b3)')
        plt.xlabel('time point (n)')
        for i in range(self.rep.get()):
            plt.plot(x, df.iloc[:, 2 + self.rep.get() + i], color='lightsteelblue')
        plt.plot(x, df.iloc[:, 2 + self.rep.get() + self.rep.get() + 1], color='royalblue')
        plt.savefig('bulkclot_volume.png', dpi=300)

        writer = pd.ExcelWriter('bulkclot_data.xlsx', engine='openpyxl')
        df.to_excel(writer, sheet_name='Data', index=False)
        writer.save()
        writer.close()



    # Closing command, clear variables
    def on_closing(self):
        """Closing command, clear variables to improve speed"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
