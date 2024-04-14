import tkinter as tk
import cv2
from PIL import Image, ImageTk

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Menu")
        self.geometry("1280x960")

        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.pages = {}
        for PageClass in [HomePage, Page1, Page2]:
            page_name = PageClass.__name__
            self.pages[page_name] = PageClass(self.container, self)
            self.pages[page_name].grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            page.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Home Page", font=("Arial", 18))
        label.pack(pady=20)

        btn1 = tk.Button(self, text="Go to Page 1", command=lambda: controller.show_page("Page1"))
        btn1.pack()

        btn2 = tk.Button(self, text="Go to Page 2", command=lambda: controller.show_page("Page2"))
        btn2.pack()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Page 1 - Video Stream", font=("Arial", 18))
        label.pack(pady=20)

        self.video_label = tk.Label(self)
        self.video_label.pack()

        self.capture = cv2.VideoCapture(0)
        self.update_video_stream()

        back_btn = tk.Button(self, text="Back to Home", command=lambda: self.back_to_home())
        back_btn.pack()

    def update_video_stream(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=frame)
            self.video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
            self.video_label.config(image=img_tk)
        self.video_label.after(10, self.update_video_stream)

    def back_to_home(self):
        # self.capture.release()
        self.controller.show_page("HomePage")


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Page 2", font=("Arial", 18))
        label.pack(pady=20)

        back_btn = tk.Button(self, text="Back to Home", command=lambda: controller.show_page("HomePage"))
        back_btn.pack()


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
