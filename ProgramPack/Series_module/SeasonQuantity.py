import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QSlider, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from ProgramPack.src.MyButton import _MyButton

class SeriesSeasonSelection(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Вибір кількості сезонів')
        self.setGeometry(400, 300, 450, 180)
        icon = QIcon(":/images/MovieIcon.jpg")
        self.setStyleSheet(
            '''
            QWidget {
        background-color: #9dadc7; /* Slightly off-white or light gray */}
            '''
        )
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)  # Заборона зміни розміру
        # Встановлюємо картинку як іконку вікна

        width = 32  # Desired width
        height = 32  # Desired height
        resized_icon = icon.pixmap(width, height).scaled(width, height)
        self.setWindowIcon(QIcon(resized_icon))

        layout = QVBoxLayout()

        self.label = QLabel('Оберіть кількість сезонів:')
        self.label.setFont(QFont("Arial", 15))
        layout.addWidget(self.label)

        self.label_value = QLabel('1')
        self.label_value.setFont(QFont("Arial", 15))
        layout.addWidget(self.label_value)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet(
        '''
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 10px;
            background: #CCCCCC;
            margin: 2px 0;
        }
        QSlider::handle:horizontal {
            background: #FF5733;
            border: 1px solid #FF5733;
            width: 18px;
            height: 18px;
            margin: -4px 0;
        border-radius: 9px;
        }
        QSlider::add-page:horizontal {
            background: #0074D9;  /* Колір під мітками */
        }
        QSlider::sub-page:horizontal {
            background: #BDBDBD;  /* Колір під "ручкою" */
        }
        '''
        )
        self.slider.setMinimum(1)
        self.slider.setMaximum(16)  # Змінено максимальне значення на 16
        self.slider.setValue(1)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        layout.addWidget(self.slider)

        self.save_button = _MyButton('Зберегти')
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.save_button.clicked.connect(self.save_to_file)

    def     on_slider_value_changed(self, value):
        if value <= 15:
            self.label_value.setText(str(value))
        else:
            self.label_value.setText('15+')

        # Анімація для збільшення текстового напису при зміні значення слайдера
        animation = QPropertyAnimation(self.label, b"geometry")
        animation.setDuration(200)
        animation.setStartValue(QRect(10, 30, 400, 30))
        animation.setEndValue(QRect(10, 30, 450, 30))
        animation.start()

    def save_to_file(self):
        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.join(project_dir, "Series_QuantitySeason.txt")

        # Open the file for writing and save the text
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.label_value.text())
            self.close()
            # QMessageBox.information(self, 'Success', 'Text saved successfully!')

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')