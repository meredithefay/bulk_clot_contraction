"""A free software created for the analysis bulk contraction assay image data

Author: Meredith Fay, Lam Lab, Georgia Institute of Technology and Emory University
Last updated: 2021-10-14 for version 1.0b1

GUI window to rotate image

See help file for an explanation of inputs, parameters, code function, and outputs

"""

import tkinter as tk
from tkinter import font
import cv2
from PIL import Image, ImageTk
import numpy as np

class RotateGUI(tk.Toplevel):

    def __init__(self, imgname, img, rep, color):
        super().__init__()

        # Fonts
        boldfont = font.Font(weight='bold')

        # Image
        self.imgname = imgname
        self.img = img
        self.rep = rep
        self.color = color

        self.angle = tk.IntVar(value=0)

        # Widgets
        self.title("Edit rotation")

        # Image name label
        name_label = tk.Label(self, text=imgname)
        name_label['font'] = boldfont
        name_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        # Replicate label
        rep_label = tk.Label(self, text="Choose rotation for " + rep, fg=color)
        rep_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        # Canvas with image
        self.img_canvas = tk.Canvas(self, width=500, height=500)
        self.img_canvas.grid(row=2, column=0, padx=5, pady=5)
        self.displayimg()
        # Angle spinbox
        thresh_spin = tk.Spinbox(
            self,
            from_=-180,
            to=180,
            increment=1,
            textvariable=self.angle,
            width=10,
            wrap=True,
            command=self.changespinbox
            )
        thresh_spin.grid(row=3, column=0, padx=5, pady=5)
        # Submit button
        submit_button = tk.Button(self, text="Submit angle", command=self.destroy)
        submit_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Row and column configures
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=2)

    # Functions

    # Resize images to fit canvas
    def displayimg(self):
        """Rotate and resize image, maintaining aspect ratio"""

        mat = self.img

        height, width = mat.shape[:2]  # image shape has 3 dimensions
        image_center = (width / 2,
                        height / 2)  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, self.angle.get(), 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0],
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rmat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

        rf = 500 / np.max((rmat.shape[0], rmat.shape[1]))
        dim = (int(rmat.shape[1] * rf), int(rmat.shape[0] * rf))
        imgr = cv2.resize(rmat, dim, interpolation=cv2.INTER_AREA)

        # Add image to canvas
        imgr_tk = ImageTk.PhotoImage(image=Image.fromarray(imgr))
        self.imgr_tk = imgr_tk  # " "
        self.img_canvas.create_image(250, 250, anchor='c', image=imgr_tk)

    def changespinbox(self):
        self.displayimg()

    def submit(self):
        self.wait_window()
        return self.angle.get()