import os
import sys
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QCheckBox, \
    QPlainTextEdit, QMessageBox, QLineEdit
from ProgramPack.src.MyButton import _MyButton

class DirectorsApp(QWidget):
    def __init__(self, directors):
        super().__init__()
        self.directors = directors
        self.selected_directors = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Вибір режисерів")
        self.setGeometry(100, 100, 400, 400)
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

        label = QLabel("Оберіть режисера:")
        layout.addWidget(label)

        self.search_input = QLineEdit()
        self.search_input.setStyleSheet(
            '''
            QLineEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
            }
            QLineEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.search_input.setPlaceholderText("Пошук режисера")
        self.search_input.textChanged.connect(self.filter_directors)
        layout.addWidget(self.search_input)

        grid_layout = QGridLayout()
        self.checkboxes = []
        row = 0
        col = 0
        for directors in self.directors:
            checkbox = QCheckBox(directors)
            checkbox.stateChanged.connect(self.update_selected_directors)
            self.checkboxes.append(checkbox)
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col == 6:
                col = 0
                row += 1

        layout.addLayout(grid_layout)

        button = _MyButton("Підтвердити")
        button.clicked.connect(self.show_selected_directors)
        layout.addWidget(button)

        self.selected_directors_text_edit = QPlainTextEdit()
        self.selected_directors_text_edit.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        layout.addWidget(self.selected_directors_text_edit)

        self.add_button = _MyButton("Додати")
        self.add_button.clicked.connect(self.add_selected_directors)
        layout.addWidget(self.add_button)


        self.setLayout(layout)

    def update_selected_directors(self, state):
        checkbox = self.sender()
        directors = checkbox.text()

        if state == 2:
            if directors not in self.selected_directors:
                self.selected_directors.append(directors)
        else:
            if directors in self.selected_directors:
                self.selected_directors.remove(directors)

    def show_selected_directors(self):
        directors_str = ", ".join(self.selected_directors)
        self.selected_directors_text_edit.setPlainText(directors_str)

    def add_selected_directors(self):
        text_to_save = self.selected_directors_text_edit.toPlainText()

        # Get the absolute path to the project's directory
        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.join(project_dir, "dataDirectors.txt")

        # Open the file for writing and save the text
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_to_save)
            self.close()

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')

    def filter_directors(self):
        search_text = self.search_input.text().strip()
        for checkbox in self.checkboxes:
            director = checkbox.text()
            if search_text.lower() in director.lower():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
