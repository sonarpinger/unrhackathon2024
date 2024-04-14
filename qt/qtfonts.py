from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

app = QApplication([])

# Get the list of available font families
font_families = QFontDatabase().families()

# Print the list of font families
for font_family in font_families:
    print(font_family)

# Remember to quit the QApplication to prevent it from hanging
app.quit()