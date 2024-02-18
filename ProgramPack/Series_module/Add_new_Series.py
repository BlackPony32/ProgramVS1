from PyQt5.QtWidgets import QDesktopWidget
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat
import Image_resource_rendered



class new_Series(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Додати новий серіал")
        self.setGeometry(0, 0, 1000, 700)

        self.center()
        self.initialize()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def initialize(self):
        self.setStyleSheet(
            '''
            QMainWindow {
                background-image: url(":/images/popcorn4.png");
            }
            '''
        )

        self.setStyleSheet(self.styleSheet())
        # Створення кнопок і додавання їх до контейнера
        button_style = '''
                    QPushButton {
                        background-color: #6C3483;  /* Пурпурно-червоний */
                        color: #FFFFFF;
                        border-style: outset;
                        padding: 2px;
                        font: bold 25px;
                        border-width: 6px;
                        border-radius: 15px;
                        border-color: #512E5F;  /* Темний пурпурно-червоний */
                    }
                    QPushButton:hover {
                        background-color: #F39C12;  /* Помаранчевий */
                    }
                    QPushButton:pressed {
                        background-color: #117A65;  /* Темний зелений */
                    }
                    '''

        button1 = _MyButton(self)
        button2 = _MyButton(self)
        button3 = _MyButton(self)

        button1.setText("Назад")
        button1.setStyleSheet(button_style)
        button1.setFixedSize(400, 70)
        button1.move(300, 400)
        button1.clicked.connect(self.open_main_Window)

        button2.setText("Новий переглянутий серіал")
        button2.setStyleSheet(button_style)
        button2.setFixedSize(400, 70)
        button2.move(45, 200)
        button2.clicked.connect(self.add_New_WatchedSeries)

        button3.setText("'Переглянути потім...'")
        button3.setStyleSheet(button_style)
        button3.setFixedSize(450, 70)
        button3.move(510, 200)
        button3.clicked.connect(self.add_Series_later)

    # назад на головне вікно

    def open_main_Window(self):
        from ProgramPack.src.MainWindow import _MainWindow
        self.main_Window = _MainWindow()
        self.main_Window.show()
        self.close()

    # додати новий переглянутий фільм
    def add_New_WatchedSeries(self):
        from ProgramPack.Series_module.New_Watched_Series import _new_Watched_Series
        self.watched_series = _new_Watched_Series()
        self.watched_series.show()
        self.close()

    # додати фільм переглянути потім
    def add_Series_later(self):
        from ProgramPack.Series_module.watch_Series_later import _new_Series_later
        self._new_Series_later = _new_Series_later()
        self._new_Series_later.show()
        self.close()