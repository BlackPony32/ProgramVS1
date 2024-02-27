import os
from decouple import config
from PyQt5.QtCore import QFileSystemWatcher, QDate, Qt, QFile, QTextStream
from PyQt5.QtWidgets import QDesktopWidget, QLineEdit, QLabel, QPlainTextEdit, QCalendarWidget, QWidget, QVBoxLayout, \
    QMessageBox
from PyQt5.QtGui import QFont
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat

class _new_Series_later(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Переглянути серіал пізніше")
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
                background-image: url(":/images/light_cinema2.png");
            }
            '''
        )
        # Set the background image using a style sheet
        self.setStyleSheet(self.styleSheet())

        #______________Тим часовий лейбл)__________________________________________________________
        TempLable = QLabel(self)
        TempLable.setFont(QFont("Arial", 41))
        TempLable.setStyleSheet("color: lightgray")
        TempLable.setText("Не затягуйте з переглядом")
        TempLable.setFixedSize(855, 105)
        TempLable.move(80, 25)

        # _____________Основні кнопки для переходу по сторінках і збереження даних в базу___________
        button1 = _MyButton(self)
        button2 = _MyButton(self)

        button1.setText("Назад")
        button1.setFixedSize(350, 60)
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
        button1.move(45, 600)
        button1.clicked.connect(self.open_newSeries)

        button2.setText("Додати серіал")
        button2.setFixedSize(350, 60)
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
        button2.move(620, 600)
        button2.clicked.connect(self.insert_data)

        # ______________Назва серіалу і поле для вводу назви_________________
        label1 = QLabel(self)
        label1.setFont(QFont("Arial", 15))
        label1.setStyleSheet("color: lightgray")
        label1.setText("Назва серіалу")
        label1.setFixedSize(200, 30)
        label1.move(45, 195)

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setPlaceholderText("Введіть назву серіалу")
        self.line_edit1.setFont(QFont("Arial", 13))
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
        self.line_edit1.setFixedSize(685, 50)
        self.line_edit1.move(290, 195)

        # ___________________Блок додавання дати_____________________________________________
        label2 = QLabel(self)
        label2.setFont(QFont("Arial", 15))
        label2.setStyleSheet("color: lightgray")
        label2.setText("Оберіть дату додавання серіалу")
        label2.setFixedSize(570, 30)
        label2.move(45, 255)

        self.labelDate = QLabel(self)
        self.labelDate.setFont(QFont("Arial", 15))
        self.labelDate.setStyleSheet("color: white")  # Set transparent background
        self.current_date = QDate.currentDate()
        # self.labelDate.setText(self.current_date.toString("dd.MM.yyyy")) #баг про накладання дат
        self.labelDate.setFixedSize(200, 45)
        self.labelDate.move(370, 305)

        self.buttonDate = _MyButton(self)
        self.buttonDate.setText("Дата додавання серіалу")
        self.buttonDate.setFixedSize(300, 45)
        self.buttonDate.move(45, 305)
        self.buttonDate.clicked.connect(self.buttonDateClicked)
        # ___________________Блок кількості сезонів_____________________________________________
        self.label22 = QLabel(self)
        self.label22.setFont(QFont("Arial", 15))
        self.label22.setStyleSheet("color: lightgray")
        self.label22.setText("Оберіть скільки сезонів в серіалі")
        self.label22.setFixedSize(570, 30)
        self.label22.move(555, 255)

        self.labelCount = QLabel(self)
        self.labelCount.setFont(QFont("Arial", 15))
        self.labelCount.setStyleSheet("color: white")
        self.labelCount.setFixedSize(200, 45)
        self.labelCount.move(850, 305)

        self.file_name40 = "Series_QuantitySeason.txt"
        self.file_path40 = os.path.join(os.getcwd(),"my_data", self.file_name40)

        self.file_watcher40 = QFileSystemWatcher()
        self.file_watcher40.addPath(self.file_path40)
        self.file_watcher40.fileChanged.connect(self.update_labelCount)
        self.update_labelCount()

        self.buttonCount = _MyButton(self)
        self.buttonCount.setText("Кількість сезонів: ")
        self.buttonCount.setFixedSize(290, 45)
        self.buttonCount.move(550, 305)
        self.buttonCount.clicked.connect(self.Season_Quantity_open)

        # _______________________Блок опису серіала____________________________________________
        label3 = QLabel(self)
        label3.setFont(QFont("Arial", 15))
        label3.setStyleSheet("color: lightgray")
        label3.setText("Короткий опис")
        label3.setFixedSize(250, 30)
        label3.move(45, 415)

        self.line_edit3 = QPlainTextEdit(self)
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
        self.line_edit3.move(270, 415)
        # ___________________________________________Кінець коду елементів__________________________

    def open_newSeries(self):
        from ProgramPack.Series_module.Add_new_Series import new_Series
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

            # self.calendar.setWindowModality(Qt.ApplicationModal)
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
    def Genres_open(self):
        from ProgramPack.src.GenresWindow import GenreSelectionApp
        import Image_resource_rc
        resource_path = ":/jsons/Genres.json"

        # Open and read the resource using QFile and QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Set the encoding to UTF-8
            import json
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
    def update_line_edit6(self):
        try:
            with open(self.file_path2, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit6.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")

    def Rating_open(self):
        from ProgramPack.src.series_movie_rating import MovieRatingApp

        self.wind = MovieRatingApp()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def update_labelCount(self):
        try:
            with open(self.file_path40, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.labelCount.setText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
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
            series_description = self.line_edit3.toPlainText()

            # Check if any of the values are empty
            if not series_name or not series_description or self.labelDate.text() == "" or self.labelCount.text() == "":
                # Show a modal message box
                QMessageBox.critical(self, "Error", "Ви пропустили одне з полів!")
                return  # Exit the function if any field is empty

            # Виконання SQL-запиту для вставки даних
            cursor = conn.cursor()

            import random
            def generate_unique_id():
                while True:
                    unique_id = random.randint(10000, 99999)

                    # Check if the generated ID exists in the database
                    cursor.execute("SELECT COUNT(*) FROM Series_later_list WHERE unique_id = %s", (unique_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        return unique_id

            unique_id = generate_unique_id()
            query = "INSERT INTO Series_later_list (unique_id, series_name, date_added,season_quantity ,series_description) VALUES (%s, %s, %s, %s, %s)"
            values = (
                unique_id,
                series_name,
                self.labelDate.text(),
                self.labelCount.text(),
                series_description
            )
            cursor.execute(query, values)

            # Застосування змін до бази даних
            conn.commit()

            # Закриття курсора та з'єднання
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Успіх", "Серіал успішно додано!")
            # ___________________Стерти лейбл сезонів____________________________________
            try:
                with open(self.file_path40, 'w', encoding='utf-8') as file:
                    pass  # Writing nothing truncates the file (clears its content)

            except Exception as e:
                print(f"Error clearing the file: {e}")
            from ProgramPack.Series_module.Watch_series_later_List import _Watch_Series_LaterList
            self._Watch_Series_LaterList = _Watch_Series_LaterList()
            self._Watch_Series_LaterList.show()
            self.close()
        except psycopg2.Error as e:
            # ___________________Стерти лейбл сезонів____________________________________
            try:
                with open(self.file_path40, 'w', encoding='utf-8') as file:
                    pass  # Writing nothing truncates the file (clears its content)

            except Exception as e:
                print(f"Error clearing the file: {e}")
            QMessageBox.critical(self, "Помилка", f"Помилка підключення до Бази даних: {e}")
