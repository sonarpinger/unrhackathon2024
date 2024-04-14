import tkinter as tk
import cv2
from PIL import Image, ImageTk

class Results(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.stats = {}

        label = tk.Label(self, text="Results", font=("Arial", 18))
        label.pack(pady=20)

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack()
        self.mode_label = tk.Label(self.stats_frame)
        self.p1_score_label = tk.Label(self.stats_frame)
        self.p2_score_label =  tk.Label(self.stats_frame)

        self.buttons = tk.Frame(self)
        self.buttons.pack(side=tk.BOTTOM, pady=(20, 30))
        self.exit_button = self.endbutton = tk.Button(self.buttons, text="Home Screen", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.X)

    def back_to_home(self):
        self.controller.play_menu_music()
        self.controller.show_page("HomePage")

    def update_labels(self):
        self.mode_label.config(text=self.stats["mode"])
        self.mode_label.pack()
        self.p1_score_label.config(text="P1 Score : " + str(int(self.stats["p1_score"])))
        self.p1_score_label.pack()
        if self.stats["mode"] == "battle":
            self.p2_score_label.config(text="P2 Score : " + str(int(self.stats["p2_score"])))            
            self.p2_score_label.pack()

    def load_stats(self, stats):
        self.stats = stats
        self.update_labels()