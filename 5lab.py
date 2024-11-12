import sys
import asyncio
import aiohttp
import aiosqlite
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

# Класс потока для выполнения HTTP-запросов
class DataLoader(QThread):
    data_loaded = pyqtSignal(list)  # Сигнал для передачи загруженных данных

    def run(self):
        asyncio.run(self.fetch_data())  # Запускаем асинхронную функцию для загрузки данных

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/posts") as response:
                data = await response.json()
                self.data_loaded.emit(data)  # Передаем данные в основной поток через сигнал

# Класс потока для асинхронного сохранения данных в SQLite
class DataSaver(QThread):
    data_saved = pyqtSignal()  # Сигнал об успешном сохранении данных

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        asyncio.run(self.save_data())  # Запускаем асинхронную функцию для сохранения данных

    async def save_data(self):
        async with aiosqlite.connect("database.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT)")
            await db.executemany("INSERT INTO posts (id, title) VALUES (?, ?)",
                                 [(item['id'], item['title']) for item in self.data])
            await db.commit()
            self.data_saved.emit()  # Передаем сигнал об успешном сохранении данных

# Основной класс приложения PyQt5
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронная загрузка данных")
        
        # Настройка элементов интерфейса
        self.layout = QVBoxLayout()

        # Кнопка для загрузки данных
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)  # Подключаем к функции load_data
        self.layout.addWidget(self.load_button)

        # Индикатор выполнения
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress)

        # Метка для отображения статуса
        self.status_label = QLabel("Ожидание загрузки данных...")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        # Создаем таймер для проверки обновлений
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(10000)  # Обновление каждые 10 секунд

    # Функция для запуска загрузки данных в отдельном потоке
    def load_data(self):
        self.progress.setValue(0)  # Обнуляем индикатор выполнения
        self.status_label.setText("Загрузка данных...")
        
        # Запускаем DataLoader
        self.loader = DataLoader()
        self.loader.data_loaded.connect(self.on_data_loaded)  # Подключаем к функции обработки данных
        self.loader.start()

    # Обработка данных после загрузки
    def on_data_loaded(self, data):
        self.status_label.setText("Сохранение данных...")
        self.progress.setValue(50)  # Обновляем индикатор выполнения

        # Запускаем DataSaver
        self.saver = DataSaver(data)
        self.saver.data_saved.connect(self.on_data_saved)  # Подключаем к функции обработки завершения сохранения
        self.saver.start()

    # Обновление интерфейса после успешного сохранения данных
    def on_data_saved(self):
        self.status_label.setText("Данные успешно сохранены в базу данных")
        self.progress.setValue(100)  # Устанавливаем индикатор выполнения на 100

# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
