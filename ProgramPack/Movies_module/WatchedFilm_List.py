import sys
import os
from decouple import config
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QDesktopWidget, QTableWidgetItem, \
    QHeaderView, QHBoxLayout, QTableWidget, QScrollArea, QMessageBox
import psycopg2
from ProgramPack.src.MyButton import _MyButton
from ProgramPack.src.MyWindowFormat import MyWindowFormat

class _WatchedFilmList(MyWindowFormat):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Список переглянутих фільмів")
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
                background-image: url(":/images/cinema1.png");
            }
            '''
        )
        label1 = QLabel(self)
        label1.setFont(QFont("Arial", 15))
        label1.setStyleSheet("color: lightgray")
        label1.setText("Пошуковий фільтр")
        label1.setFixedSize(300, 30)
        label1.move(45, 20)
        # Додайте рядок пошуку
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Введіть ключові слова для пошуку")
        self.search_input.setStyleSheet(
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
        self.search_input.move(350,20)
        self.search_input.setFixedSize(600,45)

        # Додайте прокрутний віджет
        scroll_area = QScrollArea(self)
        scroll_area.move(0, 70)
        scroll_area.setFixedSize(1000, 500)

        self.table_widget = QTableWidget(self)
        self.table_widget.setFixedSize(2000, 500)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Вимкнення горизонтальної прокрутки
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table_widget)

        # Підключення сигналу текстового поля до слоту для динамічного пошуку
        self.search_input.textChanged.connect(self.filter_table)

        self.connect_to_postgresql()

        # Додайте кнопки
        self.button1 = QPushButton("Видалити фільм", self)
        self.button1.setStyleSheet(
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
        self.button1.setFixedSize(315, 60)
        self.button1.move(45, 580)
        self.button1.clicked.connect(self.handle_delete_button_click)

        self.button2 = QPushButton("Назад", self)
        self.button2.setStyleSheet(
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
        self.button2.setFixedSize(275, 60)
        self.button2.move(365, 650)
        self.button2.clicked.connect(self.back)

        self.button3 = QPushButton("Оновити дані таблиці", self)
        self.button3.setStyleSheet(
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
        self.button3.setFixedSize(315, 60)
        self.button3.move(645, 580)
        self.button3.clicked.connect(self.update_database)

    def connect_to_postgresql(self):
        try:
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

            # Виконання SQL-запиту та виведення даних у таблиці
            cursor = conn.cursor()
            cursor.execute(
                "SELECT unique_id, movie_name, date_added, genre, movie_rating, "
                "age_restrictions, movie_description FROM New_Watched_Film_List")
            rows = cursor.fetchall()
            # Приховання стовпця з нумерацією
            self.table_widget.verticalHeader().setVisible(False)
            self.table_widget.setRowCount(len(rows))
            desired_column_count = 7
            self.table_widget.setColumnCount(desired_column_count)

            # Налаштування стилю та вигляду таблиці
            self.table_widget.setStyleSheet("""
                            QTableWidget {
                                background-color: #1e1e1e;
                                border: 1px solid #333333;
                                border-radius: 10px;
                            }

                            QTableWidget::item {
                                color: #594304;
                                background-color: #e0224b;
                                margin-top: 2px;
                                border-radius: 9px;
                                padding-left: 5px;
                                font-weight: bold;
                            }

                            QTableWidget::item:selected {
                                background-color: #ffff00;
                                color: #594304;
                                font-weight: bold;
                                font-size: 16px;
                            }
                        """)

            # Налаштування заголовків стовпців (без unique_id)
            header_labels = ["ID", "Назва фільма", "Дата додавання", "Жанр", "Оцінка фільма", "Вікові обмеження",
                             "Опис фільма"]
            self.table_widget.setHorizontalHeaderLabels(header_labels)

            header = self.table_widget.horizontalHeader()
            column_widths = [70, 200, 130, 250, 240, 400, 760]  # Встановіть бажані довжини для кожного стовпця
            for col, width in enumerate(column_widths):
                header.setSectionResizeMode(col, QHeaderView.Fixed)
                header.resizeSection(col, width)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    if j == 0:  # Якщо це перший стовпець (unique_id)
                        from IPython.external.qt_for_kernel import QtCore
                        item.setFlags(QtCore.Qt.ItemIsEnabled)  # Зробити цю комірку неклікабельною
                    else:
                        item.setToolTip(str(value))
                    self.table_widget.setItem(i, j, item)

            # Закриття курсора та з'єднання
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            self.setWindowTitle("Помилка підключення до PostgreSQL")
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            self.table_widget.setHorizontalHeaderLabels(["Error"])
            item = QTableWidgetItem(f"{e}")
            self.table_widget.setItem(0, 0, item)

    def update_database(self):
        try:
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
            cursor = conn.cursor()

            for row in range(self.table_widget.rowCount()):
                unique_id = self.table_widget.item(row, 0).text()  # Get unique_id from the first column
                movie_name = self.table_widget.item(row, 1).text()
                date_added = self.table_widget.item(row, 2).text()
                genre = self.table_widget.item(row, 3).text()
                movie_rating = self.table_widget.item(row, 4).text()
                age_restrictions = self.table_widget.item(row, 5).text()
                movie_description = self.table_widget.item(row, 6).text()

                if not genre or not movie_rating or not age_restrictions or not movie_description:
                    # Show a warning message box
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Warning)
                    msg_box.setWindowTitle("Попередження")
                    msg_box.setText("Один або декілька обов'язкових полів порожні. Зміни не будуть збережені.")
                    msg_box.exec_()
                    return  # Exit the function without updating

                # Update the corresponding row in the database based on movie_name and date_added
                cursor.execute(
                    "UPDATE New_Watched_Film_List SET movie_name = %s, date_added = %s, genre = %s, movie_rating = %s, age_restrictions = %s, movie_description = %s WHERE unique_id = %s",
                    (movie_name, date_added, genre, movie_rating, age_restrictions, movie_description, unique_id)
                )
            conn.commit()
            cursor.close()
            conn.close()
            self.setWindowTitle("Зміни збережено")
        except psycopg2.Error as e:
            self.setWindowTitle("Помилка при збереженні змін")
            print("Помилка бази даних:", e)
            import traceback
            traceback.print_exc()

    def delete_movie(self, unique_id):
        try:
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
            cursor = conn.cursor()

            # Delete the row with the specified unique_id from the database
            cursor.execute(
                "DELETE FROM New_Watched_Film_List WHERE unique_id = %s",
                (unique_id,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.setWindowTitle("Фільм видалено")
        except psycopg2.Error as e:
            self.setWindowTitle("Помилка при видаленні фільму")
            print("Помилка бази даних:", e)
            import traceback
            traceback.print_exc()

    def filter_table(self, search_text):
        for row in range(self.table_widget.rowCount()):
            row_hidden = True
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    cell_text = item.text().strip().lower()
                    if search_text.lower() in cell_text:
                        row_hidden = False
                        break
            self.table_widget.setRowHidden(row, row_hidden)
    def back(self):
        from ProgramPack.Movies_module.FilmList import _FilmList
        self.newFilm = _FilmList()
        self.newFilm.show()
        self.close()

    def handle_delete_button_click(self):
        selected_row = self.table_widget.currentRow()  # Отримати індекс вибраного рядка
        if selected_row >= 0:
            unique_id = self.table_widget.item(selected_row, 0).text()  # Отримати unique_id з першого стовпця
            self.delete_movie(unique_id)
            self.table_widget.removeRow(selected_row)  # Видалити рядок з таблиці
