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
        self.p1_score_label = tk.Label(self.stats_frame, bg="#A020F0", font=("Terminal", 28))
        self.p2_score_label = tk.Label(self.stats_frame, bg="#A020F0", font=("Terminal", 28))
        self.winner_label = tk.Label(self.stats_frame, bg="#A020F0", font=("Terminal", 50))

        self.buttons = tk.Frame(self)
        self.buttons.pack(side=tk.BOTTOM, pady=(20, 30))
        self.exit_button = self.endbutton = tk.Button(self.buttons, text="Home Screen", bg="#A020F0", font=("Terminal", 34), command=lambda: self.back_to_home())
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.X)

    def back_to_home(self):
        self.stats = {}
        self.p2_score_label.pack_forget()
        self.winner_label.pack_forget()
        self.controller.play_menu_music()
        self.controller.show_page("HomePage")

    def update_labels(self):
        p1_score = int(self.stats["p1_score"])
        self.mode_label.config(text="MODE: " + self.stats["mode"])
        self.mode_label.pack()
        self.p1_score_label.config(text="P1 Score : " + str(p1_score))
        self.p1_score_label.pack()
        if self.stats["mode"] == "battle":
            p2_score = int(self.stats["p2_score"])
            self.p2_score_label.config(text="P2 Score : " + str(p2_score))            
            self.p2_score_label.pack(fill=tk.X, expand=True)
            
            if p1_score > p2_score:
                winner_msg = "Player 1 Wins!"
            elif p1_score < p2_score:
                winner_msg = "Player 2 Wins!"
            else:
                winner_msg = "Tie!!!"
            self.winner_label.config(text = winner_msg)
            self.winner_label.pack(side=tk.BOTTOM)

    def load_stats(self, stats):
        self.stats = {}
        self.stats = stats
        self.update_labels()