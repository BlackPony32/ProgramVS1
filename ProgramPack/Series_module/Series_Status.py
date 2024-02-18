import os
import sys
from PyQt5.uic.properties import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from ProgramPack.src.MyButton import _MyButton
from PyQt5 import QtWidgets, QtCore

class _SeriesStatus(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статус Серіала")
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
            "Серіал отримав дозвіл на продовження нових сезонів чи епізодів": "Продовжено",
            "Серіал, який вже закінчився, і у нього був чіткий кінцевий епізод або завершення сюжетної лінії": "Завершений",
            "Серіал може перебувати на паузі, коли його виробництво зупинено або призупинено через різні причини": "На паузі",
            "Серіал буде завершений після певної кількості сезонів або епізодів": "Затверджений статус",
            "Серіал припинено, і не буде більше продовжений, без вирішення його сюжетної лінії": "Скасований",
            "Випуск нових епізодів призупинений, але ще не остаточно закритий.": "Неактивний",
            "Серіал зараз транслюється або продовжує випуск нових епізодів": "Активний",
            "Серіал знаходиться у стадії зйомки, монтажу та підготовки до випуску нових епізодів": "У виробництві"
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
        layout.addWidget(QLabel("Оберіть статус серіала:"))
        layout.addWidget(self.rating_combo)

        self.rating_combo.currentIndexChanged.connect(self.update_description)

        self.description_label = QLabel("Не обрано")
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
        self.description = "Не обрано"  # Default description
        self.description = self.ratings[selected_rating]
        self.description_label.setText(self.description)

    def save_to_file(self):
        project_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        file_path = os.path.join(project_dir, "Series_status.txt")
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


