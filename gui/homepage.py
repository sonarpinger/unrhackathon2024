import os
import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        print(os.getcwd())
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Dance Planet", font=("Terminal", 48), bg="#A020F0")
        label.pack(pady=20)

        image = tk.PhotoImage(file="gui/assets/images/pixelearfpurp.png")
        label2 = tk.Label(self, image=image, borderwidth=0, highlightthickness=0)
        label2.image = image
        label2.pack(pady=(20,0))

        btn1 = tk.Button(self, text="Battle Mode", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("Battle"))
        btn1.pack(anchor=tk.S, padx=(200, 10), pady=(0,30), side=tk.LEFT, expand=True)

        btn2 = tk.Button(self, text="Practice Mode", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("Practice"))
        btn2.pack(anchor=tk.S, padx=10, pady=(0,30), side=tk.LEFT, expand=True)

        btn3= tk.Button(self, text="Testing Canvases", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("CanvasPage"))
        btn3.pack(anchor=tk.S, padx=10, pady=(0,30), side=tk.LEFT, expand=True)

        btn4= tk.Button(self, text="Testing Video", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("VideoPage"))
        btn4.pack(anchor=tk.S, padx=(10, 200), pady=(0,30), side=tk.LEFT, expand=True)