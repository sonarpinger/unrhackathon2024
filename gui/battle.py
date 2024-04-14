import tkinter as tk

class Battle(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Page 2", font=("Arial", 18))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Home", command=lambda: controller.show_page("HomePage"))
        back_btn.pack()

