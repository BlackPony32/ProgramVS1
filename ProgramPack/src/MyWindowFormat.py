#from IPython.external.qt_for_kernel import QtGui, QtCore
from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic.properties import QtCore, QtGui
from PyQt5.QtCore import Qt

class MyWindowFormat(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Додаткові налаштування вашого власного вікна
        self.setWindowTitle("Моя програма PyQt5")
        self.setGeometry(0, 0, 1000, 700)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)  # Заборона зміни розміру
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)  # Заборона зміни розміру
        # Розміщення вікна посередині екрана


        # Завантажуємо картинку
        icon = QIcon(":/images/MovieIcon.jpg")

        width = 32  # Desired width
        height = 32  # Desired height
        pixmap = icon.pixmap(width, height)
        resized_icon = QIcon(pixmap)

        self.setWindowIcon(resized_icon)
        # Додаткова ініціалізація вашого власного вікна
        self.center()
        self.initialize()

    def center(self):
        # Отримання розміру екрана
        screen = QDesktopWidget().availableGeometry()
        window_size = self.geometry()

        # Розрахунок положення вікна
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        # Встановлення положення вікна
        self.move(x, y)

    def initialize(self):
        pass

    def paintEvent(self, event):
        super().paintEvent(event)  # Викликати метод paintEvent вікна MainWindow