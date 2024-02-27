import os
import sys
import json
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QCheckBox, \
    QPlainTextEdit, QMessageBox, QFileDialog
from ProgramPack.src.MyButton import _MyButton

class GenreSelectionApp(QWidget):
    def __init__(self, genres):
        super().__init__()
        self.genres = genres
        self.selected_genres = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Вибір жанрів")
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

        label = QLabel("Виберіть жанри:")
        layout.addWidget(label)

        grid_layout = QGridLayout()
        self.checkboxes = []
        row = 0
        col = 0
        for genre in self.genres:
            checkbox = QCheckBox(genre)
            checkbox.stateChanged.connect(self.update_selected_genres)
            self.checkboxes.append(checkbox)
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col == 5:
                col = 0
                row += 1

        layout.addLayout(grid_layout)

        button = _MyButton("Підтвердити")
        button.clicked.connect(self.show_selected_genres)
        layout.addWidget(button)

        self.selected_genres_text_edit = QPlainTextEdit()
        layout.addWidget(self.selected_genres_text_edit)

        self.add_button = _MyButton("Додати")
        self.add_button.clicked.connect(self.add_selected_genres)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def update_selected_genres(self, state):
        checkbox = self.sender()
        genre = checkbox.text()

        if state == 2:
            if genre not in self.selected_genres:
                self.selected_genres.append(genre)
        else:
            if genre in self.selected_genres:
                self.selected_genres.remove(genre)
    def show_selected_genres(self):
        genres_str = ", ".join(self.selected_genres)
        self.selected_genres_text_edit.setPlainText(genres_str)

    def add_selected_genres(self):
        text_to_save = self.selected_genres_text_edit.toPlainText()

    # Get the absolute path to the project's directory
        file_path = os.path.join(os.getcwd(),"my_data","dataGenres.txt")


    # Check if the file exists, create it if not
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                pass

    # Open the file for writing and save the text
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_to_save)
            self.close()

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')


