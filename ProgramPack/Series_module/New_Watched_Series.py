import json
import os
from decouple import config
from PyQt5.QtCore import Qt, QDate, QFileSystemWatcher, QFile, QTextStream
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QDesktopWidget, QLabel, QLineEdit, \
    QMessageBox, QCalendarWidget, QPlainTextEdit
from PyQt5.QtGui import QFont
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat

class _new_Watched_Series(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Новий переглянутий серіал")
        self.setGeometry(0, 0, 1000, 750)

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
                background-image: url(":/images/light_cinema2.png");
            }
            '''
        )
        # Set the background image using a style sheet

        # _____________Основні кнопки для переходу по сторінках і збереження даних в базу___________
        button1 = _MyButton(self)
        button2 = _MyButton(self)

        button1.setText("Назад")
        button1.setStyleSheet(
            '''
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
        )
        button1.setFixedSize(350, 60)
        button1.move(45, 650)
        button1.clicked.connect(self.open_newSeries)

        button2.setText("Додати серіал")
        button2.setStyleSheet(
            '''
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
        )
        button2.setFixedSize(350, 60)
        button2.move(620, 650)
        button2.clicked.connect(self.insert_data)

        # ______________Назва серіалу і поле для вводу назви_________________
        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setStyleSheet(
            '''
            QLineEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
            }
            QLineEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )

        label1 = QLabel(self)
        label2 = QLabel(self)

        label1.setFont(QFont("Arial", 15))
        label1.setStyleSheet("color: lightgray")
        label1.setText("Назва серіалу")
        label1.setFixedSize(200, 30)
        label1.move(45, 5)

        self.line_edit1.setPlaceholderText("Введіть назву серіалу")
        self.line_edit1.setFixedSize(685, 50)
        self.line_edit1.move(290, 5)

        # ___________________Блок додавання дати_____________________________________________
        label2.setFont(QFont("Arial", 15))
        label2.setStyleSheet("color: lightgray")
        label2.setText("Оберіть дату додавання серіалу")
        label2.setFixedSize(570, 30)
        label2.move(45, 55)

        self.labelDate = QLabel(self)
        self.labelDate.setFont(QFont("Arial", 15))
        self.labelDate.setStyleSheet("color: white")
        self.current_date = QDate.currentDate()
        # self.labelDate.setText(self.current_date.toString("dd.MM.yyyy")) #баг про накладання дат
        self.labelDate.setFixedSize(200, 45)
        self.labelDate.move(370, 85)

        self.buttonDate = _MyButton(self)
        self.buttonDate.setText("Дата додавання серіала")
        self.buttonDate.setFixedSize(300, 45)
        self.buttonDate.move(45, 85)
        self.buttonDate.clicked.connect(self.buttonDateClicked)
        # ___________________Блок кількості сезонів_____________________________________________
        self.label22 = QLabel(self)
        self.label22.setFont(QFont("Arial", 15))
        self.label22.setStyleSheet("color: lightgray")
        self.label22.setText("Оберіть скільки сезонів в серіалі")
        self.label22.setFixedSize(570, 30)
        self.label22.move(555, 55)

        self.labelCount = QLabel(self)
        self.labelCount.setFont(QFont("Arial", 15))
        self.labelCount.setStyleSheet("color: white")
        self.labelCount.setFixedSize(200, 45)
        self.labelCount.move(850, 85)

        self.file_name40 = "Series_QuantitySeason.txt"
        self.file_path40 = os.path.join(os.getcwd(),"ProgramPack", self.file_name40)

        self.file_watcher40 = QFileSystemWatcher()
        self.file_watcher40.addPath(self.file_path40)
        self.file_watcher40.fileChanged.connect(self.update_labelCount)
        self.update_labelCount()

        self.buttonCount = _MyButton(self)
        self.buttonCount.setText("Кількість сезонів: ")
        self.buttonCount.setFixedSize(290, 45)
        self.buttonCount.move(550, 85)
        self.buttonCount.clicked.connect(self.Season_Quantity_open)
        # _______________________________Статус серіалу________________________________
        label7 = QLabel(self)

        label7.setFont(QFont("Arial", 15))
        label7.setStyleSheet("color: lightgray")
        label7.setText("Оберіть статус серіалу")
        label7.setFixedSize(280, 30)
        label7.move(45, 135)

        self.line_edit7 = QPlainTextEdit(self)
        self.line_edit7.setPlaceholderText("Запишіть статус серіалу самостійно або оберіть з доступних")
        self.file_name3 = "Series_Status.txt"
        self.file_path3 = os.path.join(os.getcwd(),"ProgramPack", self.file_name3)

        self.file_watcher3 = QFileSystemWatcher()
        self.file_watcher3.addPath(self.file_path3)
        self.file_watcher3.fileChanged.connect(self.update_line_edit7)

        self.update_line_edit7()
        self.line_edit7.setFont(QFont("Arial", 9))  # 13 норм розмір
        self.line_edit7.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit7.setFixedSize(280, 85)
        self.line_edit7.move(45, 175)

        self.buttonStatus = _MyButton(self)
        self.buttonStatus.setText("Статус серіала")
        self.buttonStatus.setFixedSize(280, 55)
        self.buttonStatus.move(45, 270)
        self.buttonStatus.clicked.connect(self.Status_open)

        # ________________________________________Поле режисерів_______________________
        label8 = QLabel(self)
        label8.setFont(QFont("Arial", 15))
        label8.setStyleSheet("color: lightgray")
        label8.setText("Оберіть режисера")
        label8.setFixedSize(280, 30)
        label8.move(370, 135)

        self.line_edit8= QPlainTextEdit(self)
        self.line_edit8.setPlaceholderText(
            "Оберіть режисера зі списку або введіть самостійно (по замовчуванню не вказано)")
        self.file_name4 = "dataDirectors.txt"
        self.file_path4 = os.path.join(os.getcwd(),"ProgramPack", self.file_name4)

        self.file_watcher4 = QFileSystemWatcher()
        self.file_watcher4.addPath(self.file_path4)
        self.file_watcher4.fileChanged.connect(self.update_line_edit8)

        self.line_edit8.setFont(QFont("Arial", 9))  # 13 норм розмір
        self.line_edit8.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit8.setFixedSize(280, 85)
        self.line_edit8.move(370, 175)

        self.buttonTemp = _MyButton(self)
        self.buttonTemp.setText("Доступний вибір режисерів")
        self.buttonTemp.setFixedSize(280, 55)
        self.buttonTemp.move(370, 270)
        self.buttonTemp.clicked.connect(self.Directors_open)

        self.update_line_edit8()
        # _______________________________________________Поле акторів______________________________
        label9 = QLabel(self)
        label9.setFont(QFont("Arial", 15))
        label9.setStyleSheet("color: lightgray")
        label9.setText("Оберіть акторів")
        label9.setFixedSize(280, 30)
        label9.move(690, 135)

        self.line_edit9 = QPlainTextEdit(self)
        self.line_edit9.setPlaceholderText(
            "Оберіть акторів зі списку або введіть самостійно (по замовчуванню не вказано)")
        self.file_name5 = "dataActors.txt"
        self.file_path5 = os.path.join(os.getcwd(),"ProgramPack", self.file_name5)

        self.file_watcher5 = QFileSystemWatcher()
        self.file_watcher5.addPath(self.file_path5)
        self.file_watcher5.fileChanged.connect(self.update_line_edit9)

        self.line_edit9.setFont(QFont("Arial", 9))  # 13 норм розмір
        self.line_edit9.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit9.setFixedSize(280, 85)
        self.line_edit9.move(690, 175)

        self.buttonTemp2 = _MyButton(self)
        self.buttonTemp2.setText("Список доступних акторів")
        self.buttonTemp2.setFixedSize(280, 55)
        self.buttonTemp2.move(690, 270)
        self.buttonTemp2.clicked.connect(self.Actors_open)

        self.update_line_edit9()
        # _______________________________Блок жанрів серіала________________________________
        label4 = QLabel(self)

        label4.setFont(QFont("Arial", 15))
        label4.setStyleSheet("color: lightgray")
        label4.setText("Оберіть жанр серіалу")
        label4.setFixedSize(280, 30)
        label4.move(45, 345)

        self.line_edit4 = QPlainTextEdit(self)
        self.line_edit4.setPlaceholderText("Запишіть жанр серіалу самостійно або оберіть з доступних")
        self.file_name = "dataGenres.txt"
        self.file_path = os.path.join(os.getcwd(),"ProgramPack", self.file_name)

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(self.file_path)
        self.file_watcher.fileChanged.connect(self.update_line_edit4)

        self.update_line_edit4()
        self.line_edit4.setFont(QFont("Arial", 9))  # 13 норм розмір
        self.line_edit4.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit4.setFixedSize(280, 85)
        self.line_edit4.move(45, 385)

        self.buttonGanre = _MyButton(self)
        self.buttonGanre.setText("Доступні жанри")
        self.buttonGanre.setFixedSize(280, 55)
        self.buttonGanre.move(45, 480)
        self.buttonGanre.clicked.connect(self.Genres_open)

        # ________________________________________series rating(оцінка серіала)_______________________
        label5 = QLabel(self)
        label5.setFont(QFont("Arial", 15))
        label5.setStyleSheet("color: lightgray")
        label5.setText("Оберіть оцінку серіала")
        label5.setFixedSize(280, 30)
        label5.move(370, 345)

        self.line_edit5 = QPlainTextEdit(self)
        self.line_edit5.setPlaceholderText(
            "Запишіть оцінку серіала самостійно або скористайтесь запропонованою системою")
        self.file_name1 = "movie_rating_result.txt"
        self.file_path1 = os.path.join(os.getcwd(),"ProgramPack", self.file_name1)

        self.file_watcher1 = QFileSystemWatcher()
        self.file_watcher1.addPath(self.file_path1)
        self.file_watcher1.fileChanged.connect(self.update_line_edit5)

        self.line_edit5.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit5.setFixedSize(280, 85)
        self.line_edit5.move(370, 385)

        self.buttonRating = _MyButton(self)
        self.buttonRating.setText("Доступна система оцінювання")
        self.buttonRating.setFixedSize(280, 55)
        self.buttonRating.move(370, 480)
        self.buttonRating.clicked.connect(self.Rating_open)

        self.update_line_edit5()
        # _______________________________________________ age rating______________________________
        label6 = QLabel(self)
        label6.setFont(QFont("Arial", 14))
        label6.setStyleSheet("color: lightgray")
        label6.setText("Вікові обмеження")
        label6.setFixedSize(280, 30)
        label6.move(690, 345)

        self.line_edit6 = QPlainTextEdit(self)
        self.line_edit6.setPlaceholderText(
            "Введіть доповнення до вікового рейтингу або оберіть доступну")
        self.file_name2 = "movie_age_rating.txt"
        self.file_path2 = os.path.join(os.getcwd(),"ProgramPack", self.file_name2)

        self.file_watcher2 = QFileSystemWatcher()
        self.file_watcher2.addPath(self.file_path2)
        self.file_watcher2.fileChanged.connect(self.update_line_edit6)

        self.line_edit6.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit6.setFixedSize(280, 85)
        self.line_edit6.move(690, 385)

        self.buttonAge = _MyButton(self)
        self.buttonAge.setText("Доступна система рейтингу")
        self.buttonAge.setFixedSize(280, 55)
        self.buttonAge.move(690, 480)
        self.buttonAge.clicked.connect(self.Age_Rating_open)

        self.update_line_edit6()
        # _______________________Блок опису серіала____________________________________________
        self.line_edit3 = QPlainTextEdit(self)
        label3 = QLabel(self)
        label3.setFont(QFont("Arial", 15))
        label3.setStyleSheet("color: lightgray")
        label3.setText("Короткий опис")
        label3.setFixedSize(250, 30)
        label3.move(45, 555)

        self.line_edit3.setPlaceholderText("Додайте короткий опис чи замітки по серіалу")
        self.line_edit3.setStyleSheet(
            '''
            QPlainTextEdit {
                background-color: #FDFD96;  /* Світло-жовтий фон */
                border: 2px solid #FF5733;  /* Червона рамка */
                border-radius: 15px;
                padding: 10px;
                font-size: 15px;
            }
            QPlainTextEdit:focus {
                border-color: #0074D9;  /* Задаємо колір рамки при фокусі */
                background-color: #85C1E9;  /* Задаємо колір фону при фокусі */
            }
            '''
        )
        self.line_edit3.setFixedSize(700, 80)
        self.line_edit3.move(270, 555)
        # ___________________________________________Кінець коду елементів__________________________
    def open_newSeries(self):
        from ProgramPack.Series_module.Add_new_Series import new_Series

        self.cleaning()

        self.newSeries = new_Series()
        self.newSeries.show()
        self.close()
    def buttonDateClicked(self):
        self.labelDate.setText("")
        if self.buttonDate.isEnabled():
            self.show_calendar()
            self.update_label()
    def show_calendar(self):
        try:
            from PyQt5.QtGui import QIcon
            from IPython.external.qt_for_kernel import QtGui
            self.calendar = QCalendarWidget()
            icon = QIcon(":/images/MovieIcon.jpg")
            # Встановлюємо картинку як іконку вікна

            width = 32  # Desired width
            height = 32  # Desired height
            resized_icon = icon.pixmap(width, height).scaled(width, height)

            # Set the resized icon as the taskbar icon for the main window

            self.calendar.setWindowModality(Qt.ApplicationModal)
            self.calendar.clicked.connect(self.select_date)

            self.widget = QWidget()
            self.widget.setWindowTitle("Оберіть дату додавання серіалу")
            layout = QVBoxLayout()
            layout.addWidget(self.calendar)
            self.widget.setLayout(layout)
            self.widget.setWindowIcon(QtGui.QIcon(resized_icon))
            self.widget.setGeometry(200, 200, 450, 200)
            self.widget.show()
        except Exception as e:
            print("Exception in show_calendar:", e)
            QMessageBox.critical(self, "Error", "An error occurred while opening the calendar.")
    def select_date(self, date):
        try:
            self.current_date = date
            self.update_label()
            self.widget.close()
        except Exception as e:
            print("Exception in select_date:", e)
            QMessageBox.critical(self, "Error", "An error occurred while selecting the date.")
    def update_label(self):
        #self.labelDate.setText("")
        try:
            self.labelDate.setText(self.current_date.toString("dd.MM.yyyy"))
        except Exception as e:
            print("Exception in update_label:", e)
            QMessageBox.critical(self, "Error", "An error occurred while updating the label.")
    def Status_open(self):
        from ProgramPack.Series_module.Series_Status import _SeriesStatus

        self.wind = _SeriesStatus()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def Actors_open(self):
        from ProgramPack.src.Actors import ActorsApp
        resource_path = ":/jsons/Actors.json"

        # Open and read the resource using QFile and QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Set the encoding to UTF-8
            Actors_data = json.loads(stream.readAll())
            Actors = Actors_data["Actors"]
            file.close()

        self.wind = ActorsApp(Actors)
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def Directors_open(self):
        from ProgramPack.src.Directors import DirectorsApp
        resource_path = ":/jsons/_Directors.json"
        # Open and read the resource using QFile and QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Set the encoding to UTF-8
            Directors_data = json.loads(stream.readAll())
            Directors = Directors_data["Directors"]
            file.close()

        self.wind = DirectorsApp(Directors)
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def Genres_open(self):
        from ProgramPack.src.GenresWindow import GenreSelectionApp
        resource_path = ":/jsons/Genres.json"

        # Open and read the resource using QFile and QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Set the encoding to UTF-8
            genres_data = json.loads(stream.readAll())
            genres = genres_data["genres"]
            file.close()

        self.wind = GenreSelectionApp(genres)
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def update_line_edit4(self):
        #file = QFile(self.file_path)
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit4.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit5(self):
        #file1 = QFile(self.file_path1)
        try:
            with open(self.file_path1, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit5.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_labelCount(self):
        try:
            with open(self.file_path40, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.labelCount.setText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit6(self):
        try:
            with open(self.file_path2, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit6.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit7(self):
        try:
            with open(self.file_path3, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit7.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit8(self):
        try:
            with open(self.file_path4, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit8.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit9(self):
        try:
            with open(self.file_path5, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit9.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def Rating_open(self):
        from ProgramPack.src.series_movie_rating import MovieRatingApp

        self.wind = MovieRatingApp()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def Age_Rating_open(self):
        from ProgramPack.src.Age_rating import Age_MovieRatingApp

        self.wind = Age_MovieRatingApp()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def Season_Quantity_open(self):
        from ProgramPack.Series_module.SeasonQuantity import SeriesSeasonSelection

        self.wind = SeriesSeasonSelection()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def insert_data(self):
        try:
            # Підключення до бази даних PostgreSQL
            import psycopg2
            db_host = config('DB_HOST')
            db_port = config('DB_PORT')
            db_name = config('DB_NAME')
            db_user = config('DB_USER')
            db_password = config('DB_PASSWORD')
            # Підключення до бази даних PostgreSQL
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )

            # Getting text from QPlainTextEdit widgets
            series_name = self.line_edit1.text()
            series_status = self.line_edit7.toPlainText()
            series_directors = self.line_edit8.toPlainText()
            series_actors = self.line_edit9.toPlainText()
            series_genre = self.line_edit4.toPlainText()
            series_mark = self.line_edit5.toPlainText()
            age = self.line_edit6.toPlainText()
            series_description = self.line_edit3.toPlainText()

            if not series_name or not series_status or not series_directors or not series_actors or not series_genre\
                    or not series_mark or not age or not series_description or self.labelDate.text() == "" or self.labelCount.text() == "":
                # Show a modal message box
                QMessageBox.critical(self, "Error", "Ви пропустили одне з полів!")
                return  # Exit the function if any field is empty
            # Check if any of the values are empty


            # Виконання SQL-запиту для вставки даних
            cursor = conn.cursor()

            import random
            def generate_unique_id():
                while True:
                    unique_id = random.randint(10000, 99999)

                    # Check if the generated ID exists in the database
                    cursor.execute("SELECT COUNT(*) FROM Watched_Series_list WHERE unique_id = %s", (unique_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        return unique_id

            unique_id = generate_unique_id()
            query = "INSERT INTO Watched_Series_list (unique_id, series_name, date_added, season_quantity, series_status," \
                    " series_directors, series_actors, series_genre, series_mark, age, series_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
                unique_id,
                series_name,
                self.labelDate.text(),
                self.labelCount.text(),
                series_status,
                series_directors,
                series_actors,
                series_genre,
                series_mark,
                age,
                series_description
            )
            cursor.execute(query, values)

            # Застосування змін до бази даних
            conn.commit()

            # Закриття курсора та з'єднання
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Успіх", "Серіал успішно додано!")
            self.cleaning()
            from ProgramPack.Series_module.Watched_series_List import _Watched_Series_List
            self._Watched_Series_List = _Watched_Series_List()
            self._Watched_Series_List.show()
            self.close()
        except psycopg2.Error as e:
            self.cleaning()
            QMessageBox.critical(self, "Помилка", f"Помилка підключення до Бази даних: {e}")
    def cleaning(self):
        # ___________________Стерти поле жанрів_______________________________________________
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")
        # ___________________Стерти поле оцінки_______________________________________________
        try:
            with open(self.file_path1, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")
        # ___________________Стерти поле вікового рейтингу____________________________________
        try:
            with open(self.file_path2, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")

        # ___________________Стерти лейбл сезонів____________________________________
        try:
            with open(self.file_path40, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")
        # ___________________Стерти поле статусу серіала______________________________
        try:
            with open(self.file_path3, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")
        # ___________________Стерти поле режисерів____________________________________
        try:
            with open(self.file_path4, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")
        # ___________________Стерти поле акторів____________________________________
        try:
            with open(self.file_path5, 'w', encoding='utf-8') as file:
                pass  # Writing nothing truncates the file (clears its content)

        except Exception as e:
            print(f"Error clearing the file: {e}")