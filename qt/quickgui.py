import cv2
import sys
import numpy as np

from PySide6.QtGui import QGuiApplication, QImage, QPixmap
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, QTimer

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('main.qml')

class Video(QObject):
  new_frame = Signal(QImage)

  def __init__(self):
    QObject.__init__(self)
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_frame)
    # self.timer.start(1000/25) # 25 FPS
    self.timer.start(1000/5) # 1 FPS
    self.cap = cv2.VideoCapture(0)

  def update_frame(self):
    ret, frame = self.cap.read()
    if ret:
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
      cv2.imshow('frame', frame)
      cv2.waitKey(50)
      self.new_frame.emit(image)

video = Video()
engine.rootContext().setContextProperty("video", video)

print(engine.rootObjects())

sys.exit(app.exec())