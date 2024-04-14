import tkinter as tk
import cv2
from PIL import Image, ImageTk

class Dance():
    def __init__(self, name, path):
        self.name = name
        self.path = path
        

class DanceSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #middle frame to display dance selection
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.middle_frame.configure(bg="#A020F0")
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.columnconfigure(0, weight=1)
        self.label = tk.Label(self.middle_frame, text="Select a Dance", font=("Terminal", 88), bg="#A020F0", fg="#FFFFFF")
        self.label.pack(pady=(20,40))
        self.defaultDance = tk.PhotoImage(file="gui/assets/images/default.png")
        self.flossDance = tk.PhotoImage(file="gui/assets/images/floss.png")
        self.gangnamDance = tk.PhotoImage(file="gui/assets/images/gangnam_style.png")
        self.griddyDance = tk.PhotoImage(file="gui/assets/images/griddy.png")
        self.orangeDance = tk.PhotoImage(file="gui/assets/images/orange.png")
        self.takeTheL = tk.PhotoImage(file="gui/assets/images/takethel.png")

        defaultButton = tk.Button(self.middle_frame, image=self.defaultDance, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("dance-moves"))
        defaultButton.pack(side=tk.LEFT, pady=(0,40), expand=True)
        flossButton = tk.Button(self.middle_frame, image=self.flossDance, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("floss-new"))
        flossButton.pack(side=tk.LEFT, pady=(0,40), expand=True)
        gangnamButton = tk.Button(self.middle_frame, image=self.gangnamDance, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("gangnam-style"))
        gangnamButton.pack(side=tk.LEFT, pady=(0,40), expand=True)
        griddyButton = tk.Button(self.middle_frame, image=self.griddyDance, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("get-griddy"))
        griddyButton.pack(side=tk.LEFT, pady=(0,40), expand=True)
        orangeButton = tk.Button(self.middle_frame, image=self.orangeDance, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("orange-justice"))
        orangeButton.pack(side=tk.LEFT, pady=(0,40), expand=True)
        takeTheLButton = tk.Button(self.middle_frame, image=self.takeTheL, font=("Terminal", 16), bg="#A020F0", command=lambda: self.controller.show_dance("take-the-l"))
        takeTheLButton.pack(side=tk.LEFT, pady=(0,40), expand=True)

        self.lowest_frame = tk.Frame(self)
        self.lowest_frame.configure(bg="#A020F0")
        self.lowest_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        back_btn = tk.Button(self.lowest_frame, text="Back to Home", font=("Terminal", 16), bg="#A020F0", command=lambda: self.back_to_home())
        back_btn.pack(anchor=tk.S, pady=(0,30), side=tk.BOTTOM)

        #self.lower_frame = tk.Frame(self)
        #self.lower_frame.configure(bg="#A020F0")
        #self.lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #dance_labels = ["Default", "Floss", "Gangnam Style", "Griddy", "Orange Justice", "Take the L"]
        #for label in dance_labels:
        #    label = tk.Label(self.lower_frame, text=label, font=("Terminal", 16), bg="#A020F0")
        #    label.pack(side=tk.LEFT, padx=10, pady=(0,10), expand=True)

    def back_to_home(self):
        self.controller.show_page("HomePage")