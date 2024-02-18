from PyQt5.QtWidgets import QDesktopWidget
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat
import Image_resource_rendered

class _MainWindow(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ваша фільмотека")
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
        # Set the background image using a style sheet
        self.setStyleSheet(self.styleSheet())
        button_style = '''
                    QPushButton {
                        background-color: #6C3483;  /* Пурпурно-червоний */
                        color: #FFFFFF;
                        border-style: outset;
                        padding: 2px;
                        font: bold 21px;
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

        button1.setText("Додати новий фільм")
        button1.setFixedSize(450, 70)
        button1.setStyleSheet(button_style)
        button1.move(20,100)
        button1.clicked.connect(self.add_new_Film)

        button2 = _MyButton(self)
        button2.setText("Додати новий серіал")
        button2.setFixedSize(450, 70)
        button2.setStyleSheet(button_style)
        button2.move(20, 200)
        button2.clicked.connect(self.add_new_Series)

        button3 = _MyButton(self)
        button3.setText("Переглянути список фільмів")
        button3.setFixedSize(450, 70)
        button3.setStyleSheet(button_style)
        button3.move(20, 300)
        button3.clicked.connect(self.FilmList)

        button4 = _MyButton(self)
        button4.setText("Переглянути список серіалів")
        button4.setFixedSize(450, 70)
        button4.setStyleSheet(button_style)
        button4.move(20, 400)
        button4.clicked.connect(self.SeriesList)

        button5 = _MyButton(self)
        button5.setText("Вихід з програми")
        button5.setFixedSize(450, 70)
        button5.setStyleSheet(button_style)
        button5.move(20, 500)
        button5.clicked.connect(self.ProgramOut)

    def add_new_Film(self):
        from ProgramPack.Movies_module.Add_new_Film import new_Film
        self.new_film_window = new_Film()
        self.new_film_window.show()
        self.close()

    def add_new_Series(self):
        from ProgramPack.Series_module.Add_new_Series import new_Series
        self.new_series_window = new_Series()
        self.new_series_window.show()
        self.close()

    def FilmList(self):
        from ProgramPack.Movies_module.FilmList import _FilmList
        self.list = _FilmList()
        self.list.show()
        self.close()

    def SeriesList(self):
        from ProgramPack.Series_module.SeriesList import _SeriesList
        self.list = _SeriesList()
        self.list.show()
        self.close()

    def ProgramOut(self):
        self.close()