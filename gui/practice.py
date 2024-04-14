import tkinter as tk
import cv2
from PIL import Image, ImageTk

class Practice(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Helo", font=("Arial", 18))
        label.pack(pady=20)

        #side bar to show labels
        self.side_bar = tk.Frame(self)
        self.side_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.label = tk.Label(self.side_bar, text="Labels", font=("Arial", 14))
        self.label.pack()
        self.label_list = tk.Listbox(self.side_bar, height=20, width=20)
        self.label_list.pack()
        self.label_list.insert(tk.END, "Label 1")
        self.label_list.insert(tk.END, "Label 2")
        self.label_list.insert(tk.END, "Label 3")

        #video stream

        self.video_label = tk.Label(self)
        self.video_label.pack()
        # read from video file
        # self.capture = cv2.VideoCapture('C:/Users/brandonramirez/Documents/unrhackathon2024/data/test_videos/flossslow.mp4')
        
        # self.update_video_stream()

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
            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)
        else:
            print("No frame")
        self.video_label.after(10, self.update_video_stream)

    def back_to_home(self):
        # self.capture.release()
        self.controller.show_page("HomePage")