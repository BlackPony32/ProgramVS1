from PyQt5.QtWidgets import QDesktopWidget
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat

class new_Film(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Додати новий фільм")
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

        # Створення кнопок і додавання їх до контейнера
        button1 = _MyButton(self)
        button2 = _MyButton(self)
        button3 = _MyButton(self)

        button1.setText("Назад")
        button1.setFixedSize(400, 70)
        button1.setStyleSheet(button_style)
        button1.move(300, 400)
        button1.clicked.connect(self.open_main_Window)

        button2.setText("Новий переглянутий фільм")
        button2.setFixedSize(400, 70)
        button2.setStyleSheet(button_style)
        button2.move(45, 200)
        button2.clicked.connect(self.add_New_WatchedFilm)

        button3.setText("'Переглянути потім...'")
        button3.setFixedSize(450, 70)
        button3.setStyleSheet(button_style)
        button3.move(510, 200)
        button3.clicked.connect(self.add_Film_later)

    def open_main_Window(self): # назад на головне вікно
        from ProgramPack.src.MainWindow import _MainWindow
        self.main_Window = _MainWindow()
        self.main_Window.show()
        self.close()

    def add_New_WatchedFilm(self): # додати новий переглянутий фільм
        from ProgramPack.Movies_module.New_Watched_Film import _new_Watched_Film
        self.watched_film = _new_Watched_Film()
        self.watched_film.show()
        self.close()

    def add_Film_later(self): # додати фільм переглянути потім
        from ProgramPack.Movies_module.watch_Film_later import _new_Film_later
        self._new_Film_later = _new_Film_later()
        self._new_Film_later.show()
        self.close()