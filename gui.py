import os
import sys
import random
import pathlib
from PySide6 import QtCore, QtWidgets, QtGui

current_dir = pathlib.Path(__file__).parent
assets_dir = current_dir / "assets"
font_path = assets_dir / "font" / "VT323-Regular.ttf"
print(str(font_path))

class MyWidget(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    background_color = "#764abc"
    # pixelFont = QtGui.QFont(str(font_path), 30)
    pixelFontBig = QtGui.QFont("Broadway", 30)
    pixelFontSmall = QtGui.QFont("Broadway", 12)

    self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

    self.button = QtWidgets.QPushButton("Click me!")
    self.text = QtWidgets.QLabel("Hello World",
                                    alignment=QtCore.Qt.AlignCenter)
    self.text.setFont(pixelFontBig)
    self.button.setFont(pixelFontSmall)

    self.layout = QtWidgets.QVBoxLayout(self)
    self.layout.addWidget(self.text)
    self.layout.addWidget(self.button)

    self.button.clicked.connect(self.magic)

  @QtCore.Slot()
  def magic(self):
    self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1024, 768)
    widget.show()

    sys.exit(app.exec())
