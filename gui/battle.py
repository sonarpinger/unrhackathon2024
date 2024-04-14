import tkinter as tk

class Battle(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.continue_looping = True

        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }

        #side bar to show labels
        self.side_bar = tk.Frame(self)
        self.side_bar.pack(side=tk.LEFT, fill=tk.Y)

        # scores label
        self.scores_bar = tk.Frame(self.side_bar)
        self.scores_bar.pack(side=tk.TOP, pady=(30, 50))
        self.player1ScoreLabel = tk.Label(self.scores_bar, text="Player 1 Score: 0", font=("Terminal", 14))
        self.player1ScoreLabel.pack()
        self.player2ScoreLabel = tk.Label(self.scores_bar, text="Player 2 Score: 0", font=("Terminal", 14))
        self.player2ScoreLabel.pack()

        # selected dances:
        self.selected_dances_bar = tk.Frame(self.side_bar)
        self.selected_dances_bar.pack()
        self.selected_dances_title = tk.Label(self.selected_dances_bar, text = "Selected Dances", font=("Terminal", 14))
        self.selected_dances_title.pack(side=tk.TOP)
        self.selection_labels = []

        # buttons
        self.buttons_bar = tk.Frame(self.side_bar)
        self.buttons_bar.pack(side=tk.BOTTOM, pady=(20, 30))
        self.endbutton = tk.Button(self.side_bar, text="End Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X)
        self.endbutton = tk.Button(self.side_bar, text="Pause Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.loop_pause())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))
        self.startbutton = tk.Button(self.side_bar, text="Start Battle", bg="#A020F0", font=("Terminal", 14), command=lambda: self.begin_battle())
        self.startbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))

    def load_selection(self, selection):
        self.selection = selection
        print(f"selection: {self.selection}")
        for key in self.selection.keys():
            if self.selection[key]:
                dance_label = tk.Label(self.selected_dances_bar, text=key, font=("Terminal", 12))
                dance_label.pack()
                self.selection_labels.append(dance_label)

    def begin_battle(self):
        self.continue_looping = True
        pass

    def loop_pause(self):
        self.continue_looping = False
        pass

    def back_to_home(self):
        self.continue_looping = False
        # reset when leaving menu
        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }
        for label in self.selection_labels:
            label.pack_forget()
        self.selection_labels = []
        self.controller.show_page("HomePage")