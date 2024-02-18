import os
import sys
import cProfile
#from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from ProgramPack.src.MainWindow import _MainWindow

if __name__ == "__main__":
    #Робота з файлами для тимчасового збереження даних про фільм/серіал
    def clear_file(file_path):
        from pathlib import Path
        """
        Функція для очищення файлу,
        з можливістю його створення, якщо він не існує.
        """
        file_path = Path(file_path)

        # Створити папку, якщо її не існує
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Створити файл, якщо його не існує
        if not file_path.is_file():
            file_path.touch()

        # Очистити файл
        with open(file_path, 'w', encoding='utf-8') as file:
            pass

    # Очистити всі файли
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "dataGenres.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "movie_rating_result.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "movie_age_rating.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "Series_QuantitySeason.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "dataDirectors.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "dataActors.txt"))
    clear_file(os.path.join(os.getcwd(), "ProgramPack", "Series_status.txt"))

    #Запуск програми
    app = QApplication(sys.argv)

    window = _MainWindow()

    window.show()
    sys.exit(app.exec_())