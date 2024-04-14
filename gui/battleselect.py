import tkinter as tk

class BattleSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # For holding battle selection
        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }

        label = tk.Label(self, text="Battle Select", font=("Terminal", 88), bg="#A020F0", fg="#FFFFFF")
        label.pack(pady=20)

        # Middle frame to display dance selection
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.middle_frame.configure(bg="#A020F0")

        # Load images
        self.defaultDance = tk.PhotoImage(file="gui/assets/images/default.png")
        self.flossDance = tk.PhotoImage(file="gui/assets/images/floss.png")
        self.gangnamDance = tk.PhotoImage(file="gui/assets/images/gangnam_style.png")
        self.griddyDance = tk.PhotoImage(file="gui/assets/images/griddy.png")
        self.orangeDance = tk.PhotoImage(file="gui/assets/images/orange.png")
        self.takeTheL = tk.PhotoImage(file="gui/assets/images/takethel.png")

        # Define buttons and labels for each dance move
        self.dance_frames = {}
        self.buttons = {}
        self.labels = {}
        dances = ["default", "floss", "gangnam", "griddy", "orange", "takethel"]
        images = [self.defaultDance, self.flossDance, self.gangnamDance, self.griddyDance, self.orangeDance, self.takeTheL]

        for i, dance in enumerate(dances):
            # Create subframe for each dance
            frame = tk.Frame(self.middle_frame, bg="#A020F0")
            frame.pack(side=tk.LEFT, padx=10, expand=True)

            # Create button
            button = tk.Button(frame, image=images[i], bg="#A020F0", command=lambda d=dance: self.press_button(d))
            button.pack(pady=(0, 5))
            self.buttons[dance] = button

            # Create label under the button
            label = tk.Label(frame, text="Not Selected", bg="#A020F0", fg="#FFFFFF")
            label.pack()
            self.labels[dance] = label

            # Store frame for future reference or adjustments
            self.dance_frames[dance] = frame

        # Start and Back button
        self.lowest_frame = tk.Frame(self)
        self.lowest_frame.configure(bg="#A020F0")
        self.lowest_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        # Start button for proceeding with selected option
        start_btn = tk.Button(self.lowest_frame, text="Start Battle", font=("Terminal", 16), bg="#A020F0", command=self.start_battle)
        start_btn.pack(padx=10, pady=20, side=tk.TOP)
        
        back_btn = tk.Button(self.lowest_frame, text="Back to Home", font=("Terminal", 16), bg="#A020F0", command=lambda: self.back_to_home())
        back_btn.pack(anchor=tk.S, pady=(0,30), side=tk.BOTTOM)

    def start_battle(self):
        # Logic to start the battle with selected dances
        self.controller.pass_dance_selection(self.selection)
        # reset after passing
        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }

    def back_to_home(self):
        # reset when leaving menu
        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }
        for option in self.selection.keys():
            self.labels[option].config(text="Selected" if self.selection[option] else "Not Selected")
        self.controller.show_page("HomePage")

    def press_button(self, option):
        # Toggle the selection state
        self.selection[option] = not self.selection[option]
        # Update the label based on the current state
        self.labels[option].config(text="Selected" if self.selection[option] else "Not Selected")
    
    def init_selection(self):
        self.selection = {
            "default": False,
            "floss": False,
            "gangnam": False,
            "griddy": False,
            "orange": False,
            "takethel": False,
        }
