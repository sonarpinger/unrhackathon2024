from gui.practice import Practice
import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="D A N C E   P L A N E T", font=("Terminal", 48, 'bold'), bg="#A020F0", fg="#FFFFFF")
        label.pack(pady=40)

        image = tk.PhotoImage(file="gui/assets/images/pixelearfpurp.png")
        label2 = tk.Label(self, image=image, borderwidth=0, highlightthickness=0)
        label2.image = image
        label2.pack(pady=(0,0))

        btn1 = tk.Button(self, text="Battle Mode", font=("Terminal", 30), bg="#A020F0", command=lambda: controller.show_page("BattleSelect"))
        btn1.pack(anchor=tk.S, padx=(200, 10), pady=(0,50), side=tk.LEFT, expand=True)

        btn2 = tk.Button(self, text="Practice Mode", font=("Terminal", 30), bg="#A020F0", command=lambda: controller.show_page("DanceSelect"))
        btn2.pack(anchor=tk.S, padx=(10, 200), pady=(0,50), side=tk.LEFT, expand=True)

        #btn3= tk.Button(self, text="Testing Canvases", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("CanvasPage"))
        #btn3.pack(anchor=tk.S, padx=10, pady=(0,30), side=tk.LEFT, expand=True)

        #btn4= tk.Button(self, text="Testing Video", font=("Terminal", 18), bg="#A020F0", command=lambda: controller.show_page("VideoPage"))
        #btn4.pack(anchor=tk.S, padx=(10, 200), pady=(0,30), side=tk.LEFT, expand=True)
    
    def go_to_battle_select(self):
        page = self.pages.get("BattleSelect")
        page.init_selection()
        self.controller.show_page("BattleSelect")