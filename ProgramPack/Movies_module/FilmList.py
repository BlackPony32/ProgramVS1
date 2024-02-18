from PyQt5.QtWidgets import QDesktopWidget
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat

class _FilmList(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список фільмів")
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
        # фонове зображення
        self.setStyleSheet(self.styleSheet())

        self.button1 = _MyButton(self)
        self.button2 = _MyButton(self)
        self.button3 = _MyButton(self)
        button_style = '''
                    QPushButton {
                        background-color: #6C3483;  /* Пурпурно-червоний */
                        color: #FFFFFF;
                        border-style: outset;
                        padding: 2px;
                        font: bold 20px;
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

        self.button1.setText("Назад")
        self.button1.setStyleSheet(button_style)
        self.button1.setFixedSize(400, 70)
        self.button1.move(300, 400)
        self.button1.clicked.connect(self.open_main_Window)

        self.button2.setText("Список переглянутих фільмів")
        self.button2.setStyleSheet(button_style)
        self.button2.setFixedSize(400, 70)
        self.button2.move(45, 200)
        self.button2.clicked.connect(self.open_WatchedFilm_later)

        self.button3.setText("Список фільмів 'Переглянути потім...'")
        self.button3.setStyleSheet(button_style)
        self.button3.setFixedSize(450, 70)
        self.button3.move(510, 200)
        self.button3.clicked.connect(self.open_Watch_Film_later)

    def open_main_Window(self):
        from ProgramPack.src.MainWindow import _MainWindow
        self.main_Window = _MainWindow()
        self.main_Window.show()
        self.close()
    def open_WatchedFilm_later(self):
        from ProgramPack.Movies_module.WatchedFilm_List import _WatchedFilmList
        self._WatchedFilmList = _WatchedFilmList()
        self._WatchedFilmList.show()
        self.close()
    def open_Watch_Film_later(self):
        from ProgramPack.Movies_module.Watch_Film_later_List import _Watch_Film_LaterList
        self._Watch_Film_LaterList = _Watch_Film_LaterList()
        self._Watch_Film_LaterList.show()
        self.close()
