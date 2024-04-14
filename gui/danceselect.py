import tkinter as tk
import cv2
from PIL import Image, ImageTk

class DanceSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #label = tk.Label(self, text="Helo", font=("Terminal", 48), bg="#A020F0")
        #label.pack(pady=20)

        #middle frame to display dance selection
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.LEFT, fill=tk.X)
        self.middle_frame.rowconfigure(0, weight=1)
        self.middle_frame.columnconfigure(0, weight=1)
        self.label = tk.Label(self.middle_frame, text="Select a Dance", font=("Terminal", 18))
        self.label.pack()
        self.defaultDance = tk.PhotoImage(file="gui/assets/images/default.png")
        self.flossDance = tk.PhotoImage(file="gui/assets/images/floss.png")
        self.gangnamDance = tk.PhotoImage(file="gui/assets/images/gangnam_style.png")
        self.griddyDance = tk.PhotoImage(file="gui/assets/images/griddy.png")
        self.orangeDance = tk.PhotoImage(file="gui/assets/images/orange.png")
        self.takeTheL = tk.PhotoImage(file="gui/assets/images/takethel.png")
        dances = [self.defaultDance, self.flossDance, self.gangnamDance, self.griddyDance, self.orangeDance, self.takeTheL]
        for dance in dances:
            #dance.
            label = tk.Label(self.middle_frame, image=dance, borderwidth=0, highlightthickness=0)
            label.pack(side=tk.LEFT, padx=10, pady=(0,10), expand=True)

        #self.endbutton = tk.Button(self.side_bar, text="End Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        #self.endbutton.pack(side=tk.BOTTOM, fill=tk.X)
        #self.endbutton = tk.Button(self.side_bar, text="Restart Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.loop_reenable())
        #self.endbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))
        #self.startbutton = tk.Button(self.side_bar, text="Start Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.update_video_streams())
        #self.startbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))

        #self.label_list.i#se

        back_btn = tk.Button(self, text="Back to Home", command=lambda: self.back_to_home())
        back_btn.pack()

    def back_to_home(self):
        self.controller.show_page("HomePage")