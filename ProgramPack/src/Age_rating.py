import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from ProgramPack.src.MyButton import _MyButton

class Age_MovieRatingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Віковий рейтинг фільмів")
        self.setGeometry(200, 200, 400, 150)
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

        self.ratings = {
            "Не обрано": "Не обрано",
            "G": "G - Для всіх",
            "PG": "PG - Батькам рекомендовано",
            "PG-13": "PG-13 Для дітей від 13 років",
            "R": "R - Для дорослих",
            "NC-17": "NC-17 Тільки для дорослих"
        }

        layout = QVBoxLayout()

        self.rating_combo = QComboBox()
        self.rating_combo.setStyleSheet(
        '''
        QComboBox {
            background-color: #FFFFFF;  /* Білий фон */
            border: 1px solid #BDBDBD;  /* Сіра рамка товщиною 1px */
            border-radius: 5px;
            padding: 6px;
            font-size: 14px;
            color: #333333;  /* Чорний колір тексту */
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #BDBDBD;  /* Сіра рамка товщиною 1px */
            border-left-style: solid;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            background: #FDFD96;  /* Жовтий фон для стрілки вниз */
        }
        QComboBox::down-arrow {
            image: url(:/images/Down_arrow.png);  /* Зображення для стрілки вниз */
            width: 20px;
            height: 20px;
        }
        '''
        )

        self.rating_combo.addItems(self.ratings.keys())
        layout.addWidget(QLabel("Виберіть віковий рейтинг фільму:"))
        layout.addWidget(self.rating_combo)

        self.rating_combo.currentIndexChanged.connect(self.update_description)

        self.description_label = QLabel("Не обрано")
        self.description_label.setStyleSheet(
            '''
            QLabel {
            background-color: #FFFFFF;  /* Білий фон */
                border: 1px solid #BDBDBD;  /* Сіра рамка товщиною 1px */
                border-radius: 5px;
                padding: 6px;
                font-size: 14px;
                color: #333333;  /* Чорний колір тексту */
            }
            ''')
        layout.addWidget(self.description_label)

        hbox = QHBoxLayout()
        self.submit_button = _MyButton("Зберегти результат")
        self.submit_button.clicked.connect(self.save_to_file)
        hbox.addWidget(self.submit_button)

        layout.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_description(self):
        selected_rating = self.rating_combo.currentText()
        self.description = self.ratings[selected_rating]
        self.description_label.setText(self.description)

    #покищо не працює
    def add_selected_genres(self):
        text_to_save = self.selected_genres_text_edit.toPlainText()

    # Get the absolute path to the project's directory
        file_path = os.path.join(os.getcwd(),"my_data","movie_age_rating.txt")
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
            
    def save_to_file(self):
        file_path = os.path.join(os.getcwd(),"my_data","movie_age_rating.txt")
        self.update_description()
        # Open the file for writing and save the text
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.description)
            self.close()
            # QMessageBox.information(self, 'Success', 'Text saved successfully!')

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')


