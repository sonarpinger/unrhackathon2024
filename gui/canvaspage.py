import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CanvasPage(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.Labelframe1 = tk.LabelFrame(self)
    self.Labelframe1.place(x=10, y=0, height=955, width=350)
    self.Labelframe1.configure(relief='groove')
    self.Labelframe1.configure(foreground="#000000")
    self.Labelframe1.configure(text='''Labelframe''')
    self.Labelframe1.configure(background="#d9d9d9")
    self.Labelframe1.configure(highlightbackground="#d9d9d9")
    self.Labelframe1.configure(highlightcolor="#000000")

    # self.Canvas1 = tk.Canvas(self)
    # self.Canvas1.place(x=370, y=10, height=943, width=1063)
    # self.Canvas1.configure(background="#d9d9d9")
    # self.Canvas1.configure(borderwidth="2")
    # self.Canvas1.configure(highlightbackground="#d9d9d9")
    # self.Canvas1.configure(highlightcolor="#000000")
    # self.Canvas1.configure(insertbackground="#000000")
    # self.Canvas1.configure(relief="ridge")
    # self.Canvas1.configure(selectbackground="#d9d9d9")
    # self.Canvas1.configure(selectforeground="black")

    # self.Canvas2 = tk.Canvas(self.Canvas1)
    # self.Canvas2.place(x=630, y=670, height=273, width=433)
    # self.Canvas2.configure(background="#d9d9d9")
    # self.Canvas2.configure(borderwidth="2")
    # self.Canvas2.configure(highlightbackground="#d9d9d9")
    # self.Canvas2.configure(highlightcolor="#000000")
    # self.Canvas2.configure(insertbackground="#000000")
    # self.Canvas2.configure(relief="ridge")
    # self.Canvas2.configure(selectbackground="#d9d9d9")
    # self.Canvas2.configure(selectforeground="black")

    self.video_label = tk.Label(self)
    self.video_label.place(x=370, y=10, height=943, width=1063)

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
  # top.geometry("1440x960+452+36")
  # top.minsize(120, 1)
  # top.maxsize(3844, 1061)
  # top.resizable(0,  0)
  # top.title("Toplevel 0")
  # top.configure(background="#d9d9d9")
  # top.configure(highlightbackground="#d9d9d9")
  # top.configure(highlightcolor="#000000")

  # self.top = top

  # self.Labelframe1 = tk.LabelFrame(self.top)
  # self.Labelframe1.place(x=10, y=0, height=955, width=350)
  # self.Labelframe1.configure(relief='groove')
  # self.Labelframe1.configure(foreground="#000000")
  # self.Labelframe1.configure(text='''Labelframe''')
  # self.Labelframe1.configure(background="#d9d9d9")
  # self.Labelframe1.configure(highlightbackground="#d9d9d9")
  # self.Labelframe1.configure(highlightcolor="#000000")

  # self.Canvas1 = tk.Canvas(self.top)
  # self.Canvas1.place(x=370, y=10, height=943, width=1063)
  # self.Canvas1.configure(background="#d9d9d9")
  # self.Canvas1.configure(borderwidth="2")
  # self.Canvas1.configure(highlightbackground="#d9d9d9")
  # self.Canvas1.configure(highlightcolor="#000000")
  # self.Canvas1.configure(insertbackground="#000000")
  # self.Canvas1.configure(relief="ridge")
  # self.Canvas1.configure(selectbackground="#d9d9d9")
  # self.Canvas1.configure(selectforeground="black")

  # self.Canvas2 = tk.Canvas(self.Canvas1)
  # self.Canvas2.place(x=630, y=670, height=273, width=433)
  # self.Canvas2.configure(background="#d9d9d9")
  # self.Canvas2.configure(borderwidth="2")
  # self.Canvas2.configure(highlightbackground="#d9d9d9")
  # self.Canvas2.configure(highlightcolor="#000000")
  # self.Canvas2.configure(insertbackground="#000000")
  # self.Canvas2.configure(relief="ridge")
  # self.Canvas2.configure(selectbackground="#d9d9d9")
  # self.Canvas2.configure(selectforeground="black")