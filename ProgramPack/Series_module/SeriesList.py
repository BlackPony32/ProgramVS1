from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFont
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat



class _SeriesList(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список серіалів")
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

        button1 = _MyButton(self)
        button2 = _MyButton(self)
        button3 = _MyButton(self)

        button1.setText("Назад")
        button1.setStyleSheet(button_style)
        button1.setFixedSize(400, 70)
        button1.move(300, 400)
        button1.clicked.connect(self.open_main_Window)

        button2.setText("Список переглянутих серіалів")
        button2.setStyleSheet(button_style)
        button2.setFixedSize(400, 70)
        button2.move(45, 200)
        button2.clicked.connect(self.Watched_SeriesList_open)

        button3.setText("Список серіалів 'Переглянути потім...'")
        button3.setStyleSheet(button_style)
        button3.setFixedSize(450, 70)
        button3.move(510, 200)
        button3.clicked.connect(self.Watch_Series_laterList_open)

    def open_main_Window(self):
        from ProgramPack.src.MainWindow import _MainWindow
        self.main_Window = _MainWindow()
        self.main_Window.show()
        self.close()

    def Watched_SeriesList_open(self):
        from ProgramPack.Series_module.Watched_series_List import _Watched_Series_List
        self._Watched_Series_List = _Watched_Series_List()
        self._Watched_Series_List.show()
        self.close()

    def Watch_Series_laterList_open(self):
        from ProgramPack.Series_module.Watch_series_later_List import _Watch_Series_LaterList
        self._Watch_Series_LaterList = _Watch_Series_LaterList()
        self._Watch_Series_LaterList.show()
        self.close()