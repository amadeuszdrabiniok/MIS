# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys


from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from Klient import Klient
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Klient()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
