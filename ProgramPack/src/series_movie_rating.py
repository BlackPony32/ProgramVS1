import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic.properties import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, \
    QMessageBox
from ProgramPack.src.MyButton import _MyButton

class MovieRatingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оцінка фільмів-серіалів")
        self.setGeometry(200, 200, 600, 300)
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
            1: "Жахливо! Не рекомендую.",
            2: "Дуже поганий.",
            3: "Слабенький, не вразив.",
            4: "Звичайний, нічого особливого.",
            5: "Непоганий, можна подивитися.",
            6: "Хороший, рекомендую.",
            7: "Дуже хороший, вартий уваги.",
            8: "Чудовий! Провів час із задоволенням.",
            9: "Відмінний! Велике задоволення.",
            10: "Шедевр! Обов'язково перегляну ще раз!"
        }

        layout = QVBoxLayout()

        for rating, comment in self.ratings.items():
            hbox = QHBoxLayout()

            comment_label = QLabel(comment)
            comment_label.setStyleSheet(
            '''
            QLabel {
            background-color: #FFFFFF;  /* Білий фон */
                border: 1px solid #BDBDBD;  /* Сіра рамка товщиною 1px */
                border-radius: 5px;
                padding: 6px;
                font-size: 14px;
                color: #333333;  /* Чорний колір тексту */
            }
            '''
            )
            hbox.addWidget(comment_label)

            rating_button = _MyButton(f"{rating}/10")
            rating_button.clicked.connect(self.show_result)
            hbox.addWidget(rating_button)

            layout.addLayout(hbox)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        save_button = _MyButton("Зберегти результат")
        save_button.clicked.connect(self.save_to_file)
        layout.addWidget(save_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_result(self):
        button = self.sender()
        rating = int(button.text().split("/")[0])
        comment = self.ratings[rating]
        self.result_label.setText(f"Ви обрали оцінку: {button.text()}\n{comment}")

        self.current_result = f"Ви обрали оцінку: {button.text()}\n{comment}"

    def save_to_file(self):
        file_path = os.path.join(os.getcwd(),"my_data","movie_rating_result.txt")

        # Open the file for writing and save the text
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.current_result)
            self.close()
            # QMessageBox.information(self, 'Success', 'Text saved successfully!')

        except Exception as e:
            print(f"Error writing to the file: {e}")
            QMessageBox.critical(self, 'Error', f'Error saving text:\n{str(e)}')



