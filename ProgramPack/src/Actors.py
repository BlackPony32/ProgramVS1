import os
import sys
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QIcon

from ProgramPack.src.MyButton import _MyButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, \
    QPlainTextEdit, QMessageBox, QFileDialog, QLineEdit


class ActorsApp(QWidget):
    def __init__(self, actors):
        super().__init__()
        self.actors = actors
        self.selected_actors = []

        self.init_ui()

    def init_ui(self):
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
        self.setWindowTitle("Вибір акторів")
        self.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()

        label = QLabel("Оберіть акторів:")
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
        self.search_input.setPlaceholderText("Пошук акторів")
        self.search_input.textChanged.connect(self.filter_actors)
        layout.addWidget(self.search_input)

        grid_layout = QGridLayout()
        self.checkboxes = []
        row = 0
        col = 0
        for actors in self.actors:
            checkbox = QCheckBox(actors)
            checkbox.stateChanged.connect(self.update_selected_actors)
            self.checkboxes.append(checkbox)
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col == 8:
                col = 0
                row += 1

        layout.addLayout(grid_layout)

        button = _MyButton("Підтвердити")
        button.clicked.connect(self.show_selected_actors)
        layout.addWidget(button)

        self.selected_actors_text_edit = QPlainTextEdit()
        self.selected_actors_text_edit.setStyleSheet(
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
        layout.addWidget(self.selected_actors_text_edit)

        self.add_button = _MyButton("Додати")
        self.add_button.clicked.connect(self.add_selected_actors)
        layout.addWidget(self.add_button)


        self.setLayout(layout)

    def update_selected_actors(self, state):
        checkbox = self.sender()
        actors = checkbox.text()

        if state == 2:
            if actors not in self.selected_actors:
                self.selected_actors.append(actors)
        else:
            if actors in self.selected_actors:
                self.selected_actors.remove(actors)

    def show_selected_actors(self):
        actors_str = ", ".join(self.selected_actors)
        self.selected_actors_text_edit.setPlainText(actors_str)

    def add_selected_actors(self):
        text_to_save = self.selected_actors_text_edit.toPlainText()

        # Отримати абсолютний шлях до каталогу проекту
        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.join(project_dir, "dataActors.txt")

        # Відкрийте файл для запису і збережіть текст
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_to_save)
            self.close()
            #QMessageBox.information(self, 'Success', 'Text saved successfully!')

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')

    def filter_actors(self):
        search_text = self.search_input.text().strip()
        for checkbox in self.checkboxes:
            director = checkbox.text()
            if search_text.lower() in director.lower():
                checkbox.setVisible(True)
            else:
                checkbox.setVisible(False)
