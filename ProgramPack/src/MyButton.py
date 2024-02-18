from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton

class _MyButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Встановлюємо стилі кнопки
        self.setStyleSheet(
            '''
            QPushButton {
                background-color: #6C3483;  /* Пурпурно-червоний */
                color: #FFFFFF;
                border-style: outset;
                padding: 2px;
                font: bold 15px;
                border-width: 6px;
                border-radius: 16px;
                border-color: #512E5F;  /* Темний пурпурно-червоний */
            }
            QPushButton:hover {
                background-color: #F39C12;  /* Помаранчевий */
            }
            QPushButton:pressed {
                background-color: #b80641;  /* Темний зелений */
            }
            '''
        )

        # Ініціалізуємо анімаційні властивості
        self.current_color = QColor(255, 0, 0)

    def setColor(self, color):
        self.current_color = color
        self.update()

    def getColor(self):
        return self.current_color

    color = property(getColor, setColor)
