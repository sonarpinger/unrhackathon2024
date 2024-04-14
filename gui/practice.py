import tkinter as tk
import cv2
from PIL import Image, ImageTk

class Practice(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.continue_looping = True

        #label = tk.Label(self, text="Helo", font=("Terminal", 48), bg="#A020F0")
        #label.pack(pady=20)

        #side bar to show labels
        self.side_bar = tk.Frame(self)
        self.side_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.scoreLabel = tk.Label(self.side_bar, text="Score: 0", font=("Terminal", 14))
        self.scoreLabel.pack()

        self.endbutton = tk.Button(self.side_bar, text="End Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.back_to_home())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X)
        self.endbutton = tk.Button(self.side_bar, text="Restart Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.loop_reenable())
        self.endbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))
        self.startbutton = tk.Button(self.side_bar, text="Start Game", bg="#A020F0", font=("Terminal", 14), command=lambda: self.update_video_streams())
        self.startbutton.pack(side=tk.BOTTOM, fill=tk.X, pady=(0,20))

        self.video_label = tk.Label(self)
        self.video_label.place(x=320, y=25, width=1440, height=960)
        self.webcam_video_label = tk.Label(self)
        self.webcam_video_label.place(x=320, y=25, width=320, height=240)
        self.capture_webcam = cv2.VideoCapture(0)
        self.capture_video = cv2.VideoCapture('gui/assets/videos/flossslow.mp4')

    def update_video_streams(self):
        ret1, web_frame = self.capture_webcam.read()
        ret2, vid_frame = self.capture_video.read()
        if ret1 and ret2:
            web_frame = cv2.cvtColor(web_frame, cv2.COLOR_BGR2RGB)
            web_frame = Image.fromarray(web_frame)
            web_frame = web_frame.resize((320, 240))
            img_tk = ImageTk.PhotoImage(image=web_frame)
            self.webcam_video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
            self.webcam_video_label.config(image=img_tk)

            vid_frame = cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGB)
            vid_frame = Image.fromarray(vid_frame)
            vid_frame = vid_frame.resize((1440, 960))
            img_tk = ImageTk.PhotoImage(image=vid_frame)
            self.video_label.img_tk = img_tk  # Keep reference to avoid garbage collection
            self.video_label.config(image=img_tk)
            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)
        else:
            self.capture_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        if self.continue_looping:
            self.webcam_video_label.after(10, self.update_video_streams)
        else:
            self.video_label.after_cancel(self.update_video_streams)

    def loop_reenable(self):
        if not self.continue_looping:
            self.continue_looping = True
            self.capture_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_streams()
            self.scoreLabel.config(text="Score: 0")

    def update_score(self):
        pass

    def load_dance(self):
        pass

    def back_to_home(self):
        self.continue_looping = False
        self.controller.show_page("HomePage")