import json
import os
from decouple import config
from PyQt5.QtCore import Qt, QDate, QFileSystemWatcher, QFile, QTextStream
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QDesktopWidget, QLabel, QLineEdit, \
    QMessageBox, QCalendarWidget, QPlainTextEdit
from PyQt5.QtGui import QFont
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat
import Image_resource_rendered
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsWidget

class _new_Watched_Film(MyWindowFormat):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Новий переглянутий фільм")
        self.setGeometry(0, 0, 1000, 700)

        self.center()
        self.initialize()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    def initialize(self):
        #код,що додає фоновий градієнт лише до головного вікна
        self.central_widget = QWidget(self)  # Create the central widget
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: qlineargradient(x1: 0,y1: 0,x2: 1,y2: 1,stop: 0 #1A1C20, stop: 0.25 #34495e,stop: 1 #4B5C77,);box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); border-radius: 5px;")

        #self.setStyleSheet("background-color: qlineargradient(x1: 0, x2: 1, stop: 0 #250002, stop: 1 #7f0014);")
        """self.setStyleSheet(
            '''
            QMainWindow {
                background-image: url(":/images/cinema1.png");
            }
            '''
        )"""
        # фонове зображення
        self.setStyleSheet(self.styleSheet())

        #_____________Основні кнопки для переходу по сторінках і збереження даних в базу___________
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
        button1.move(45, 600)
        button1.clicked.connect(self.open_newFilm)

        button2.setText("Додати фільм")
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
        button2.move(620, 600)
        button2.clicked.connect(self.insert_data)

        #___________________Лейбл про анекдот та поле для виводу випадкового анегдоту_____________________________
        label0 = QLabel(self)
        labelAnec = QPlainTextEdit(self)

        label0.setFont(QFont("Arial", 15))
        label0.setStyleSheet("color: lightgray")
        label0.setText("Невеликий анекдот на тематику фільмів (згенеровано АІ)")
        label0.setFixedSize(795, 30)
        label0.move(45, 15)

        self.generate_random_anecdote()
        random_joke = self.generate_random_anecdote()
        labelAnec.setReadOnly(True)
        labelAnec.setStyleSheet(
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
        labelAnec.setPlainText(random_joke)
        labelAnec.setFixedSize(930, 70)
        labelAnec.move(45, 45)

        #______________Назва фільму і поле для вводу назви_________________
        self.line_edit1 = QLineEdit(self)
        label1 = QLabel(self)
        label2 = QLabel(self)
        self.line_edit3 = QPlainTextEdit(self)
        label3 = QLabel(self)

        label1.setFont(QFont("Arial", 15))
        label1.setStyleSheet("color: lightgray")
        label1.setText("Назва фільму")
        label1.setFixedSize(200, 30)
        label1.move(45, 120)

        self.line_edit1.setPlaceholderText("Введіть назву фільму")
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
        self.line_edit1.move(290, 120)

        # ___________________Блок дати додавання дати_____________________________________________
        label2.setFont(QFont("Arial", 15))
        label2.setStyleSheet("color: lightgray")
        label2.setText("Оберіть дату додавання фільму")
        label2.setFixedSize(570, 30)
        label2.move(45, 175)

        self.labelDate = QLabel(self)
        self.labelDate.setFont(QFont("Arial", 15))
        self.labelDate.setStyleSheet("color: white")
        self.current_date = QDate.currentDate()
        #self.labelDate.setText(self.current_date.toString("dd.MM.yyyy")) #баг про накладання дат
        self.labelDate.setFixedSize(200, 45)
        self.labelDate.move(300, 205)

        self.buttonDate = _MyButton(self)
        self.buttonDate.setText("Дата додавання")
        self.buttonDate.setFixedSize(250, 45)
        self.buttonDate.move(45, 205)
        self.buttonDate.clicked.connect(self.buttonDateClicked)
        # _______________________Блок опису фільму____________________________________________
        label3.setFont(QFont("Arial", 15))
        label3.setStyleSheet("color: lightgray")
        label3.setText("Короткий опис")
        label3.setFixedSize(250, 30)
        label3.move(45, 265)

        self.line_edit3.setPlaceholderText("Додайте короткий опис чи замітки по фільму")
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
        self.line_edit3.move(270, 265)

        #_________________Блок опису жанру фільму______________________
        label4 = QLabel(self)
        label4.setFont(QFont("Arial", 15))
        label4.setStyleSheet("color: lightgray")
        label4.setText("Оберіть жанр фільму")
        label4.setFixedSize(280, 30)
        label4.move(45, 345)

        self.file_name = "dataGenres.txt"
        self.file_path = os.path.join(os.getcwd(),"ProgramPack", self.file_name)
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(self.file_path)
        self.file_watcher.fileChanged.connect(self.update_line_edit4)



        self.line_edit4 = QPlainTextEdit(self)
        self.line_edit4.setPlaceholderText("Запишіть жанр фільму самостійно або оберіть з доступних")
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
        self.update_line_edit4()

        self.buttonGanre = _MyButton(self)
        self.buttonGanre.setText("Доступні жанри")
        self.buttonGanre.setFixedSize(280, 55)
        self.buttonGanre.move(45, 480)
        self.buttonGanre.clicked.connect(self.Genres_open)

        #________________________________________film rating(оцінка фільму)_______________________
        label5 = QLabel(self)
        label5.setFont(QFont("Arial", 15))
        label5.setStyleSheet("color: lightgray")
        label5.setText("Оберіть оцінку фільму")
        label5.setFixedSize(280, 30)
        label5.move(370, 345)

        self.line_edit5 = QPlainTextEdit(self)
        self.line_edit5.setPlaceholderText("Запишіть оцінку фільму самостійно або скористайтесь запропонованою системою")
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
        #_______________________________________________ age rating______________________________
        label6 = QLabel(self)
        label6.setFont(QFont("Arial", 15))
        label6.setStyleSheet("color: lightgray")
        label6.setText("Віковий рейтинг фільму")
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
        #___________________________________________Кінець коду елементів__________________________

    def show_calendar(self):
        try:
            from PyQt5.QtGui import QIcon
            from IPython.external.qt_for_kernel import QtGui
            self.calendar = QCalendarWidget()
            icon = QIcon(":/images/MovieIcon.jpg")
            # Встановлюємо картинку як іконку вікна

            width = 32  # Бажана ширина
            height = 32  # Бажана висота
            resized_icon = icon.pixmap(width, height).scaled(width, height)

            # Встановіть іконки зміненого розміру як іконку панелі завдань для головного вікна

            #self.calendar.setWindowModality(Qt.ApplicationModal)

            self.calendar.setWindowModality(Qt.ApplicationModal)
            self.calendar.clicked.connect(self.select_date)

            self.widget = QWidget()
            self.widget.setWindowTitle("Оберіть дату додавання фільму")
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
    def buttonDateClicked(self):
        self.labelDate.setText("")
        if self.buttonDate.isEnabled():
            self.show_calendar()
            self.update_label()
    def generate_random_anecdote(self):
        import json
        import random
        import Image_resource_rendered
        resource_path = ":/jsons/Filmanecdotes.json"

        # Відкрити та прочитати ресурс з допомогою QFile та QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Встановіть кодування UTF-8
            anecdotes = json.loads(stream.readAll())
            file.close()
        random_anecdote = random.choice(anecdotes)

        return random_anecdote['text']
    def open_newFilm(self):
        from ProgramPack.Movies_module.Add_new_Film import new_Film
        self.cleaning()

        self.newFilm = new_Film()
        self.newFilm.show()
        self.close()
    def Genres_open(self):
        from ProgramPack.src.GenresWindow import GenreSelectionApp
        import Image_resource_rendered
        resource_path = ":/jsons/Genres.json"

        # Відкрити та прочитати ресурс з допомогою QFile та QTextStream
        file = QFile(resource_path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")  # Встановіть кодування UTF-8
            genres_data = json.loads(stream.readAll())
            genres = genres_data["genres"]
            file.close()

        self.wind = GenreSelectionApp(genres)
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()

    def update_line_edit4(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            self.line_edit4.setPlainText(text_content)

        except Exception as e:
            print(f"Error reading the file: {e}")
    def update_line_edit5(self):
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
    def Age_Rating_open(self):
        from ProgramPack.src.Age_rating import Age_MovieRatingApp

        self.wind = Age_MovieRatingApp()
        self.wind.setWindowModality(Qt.ApplicationModal)
        self.wind.show()
    def insert_data(self):
        try:
            # Підключення до бази даних PostgreSQL
            import psycopg2
            # Зчитуємо значення змінних середовища
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

            # Отримання тексту з віджетів QPlainTextEdit
            movie_name = self.line_edit1.text()
            genre = self.line_edit4.toPlainText()
            movie_rating = self.line_edit5.toPlainText()
            age_restrictions = self.line_edit6.toPlainText()
            movie_description = self.line_edit3.toPlainText()

            if not movie_name or not  genre \
                    or not movie_rating or not age_restrictions or not movie_description or self.labelDate.text() == "":
                # Показати модальне вікно повідомлення
                QMessageBox.critical(self, "Error", "Ви пропустили одне з полів!")
                return  # Вийти з функції, якщо будь-яке поле пусте
            # Перевірте, чи жодне зі значень не порожнє

            # Виконання SQL-запиту для вставки даних
            cursor = conn.cursor()

            import random
            def generate_unique_id():
                while True:
                    unique_id = random.randint(10000, 99999)

                    # Перевірити, чи згенерований ідентифікатор існує в базі даних
                    cursor.execute("SELECT COUNT(*) FROM New_Watched_Film_List WHERE unique_id = %s", (unique_id,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        return unique_id

            unique_id = generate_unique_id()
            query = "INSERT INTO New_Watched_Film_List (unique_id, movie_name, date_added, genre, movie_rating, age_restrictions, movie_description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                unique_id,
                movie_name,
                self.labelDate.text(),
                genre,
                movie_rating,
                age_restrictions,
                movie_description
            )
            cursor.execute(query, values)

            # Застосування змін до бази даних
            conn.commit()

            # Закриття курсора та з'єднання
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Успіх", "Фільм успішно додано!")
            self.cleaning()
            from ProgramPack.Movies_module.WatchedFilm_List import _WatchedFilmList
            self._WatchedFilmList = _WatchedFilmList()
            self._WatchedFilmList.show()
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


