from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
import sys

from sidebar import MoodMateApp

app = QApplication(sys.argv)

window = MoodMateApp()

window.show()
app.exec()
