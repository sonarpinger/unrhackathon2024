import sys
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

class Video(QObject):
    new_frame = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.capture = cv2.VideoCapture(0)  # Change the index if necessary

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(1000 // 30)  # Update at 30 FPS

    def get_frame(self):
        ret, frame = self.capture.read()
        if ret:
            self.new_frame.emit(frame)

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()

# Create the video object and expose it to QML
video = Video()
engine.rootContext().setContextProperty("video", video)

engine.load(QUrl.fromLocalFile("main.qml"))
if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec_())