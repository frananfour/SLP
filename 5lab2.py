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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_data())

    async def fetch_data(self):
        await asyncio.sleep(1)  # Имитация задержки
        async with aiohttp.ClientSession() as session:
            async with session.get("https://jsonplaceholder.typicode.com/posts") as response:
                data = await response.json()
                self.data_loaded.emit(data)


# Класс потока для асинхронного сохранения данных в SQLite
class DataSaver(QThread):
    data_saved = pyqtSignal()  # Сигнал об успешном сохранении данных

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.save_data())

    async def save_data(self):
        await asyncio.sleep(1)  # Имитация задержки
        async with aiosqlite.connect("database.db") as db:
            await db.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT)")
            await db.executemany(
                "INSERT OR IGNORE INTO posts (id, title) VALUES (?, ?)",
                [(item['id'], item['title']) for item in self.data if 'id' in item and 'title' in item]
            )
            await db.commit()
            self.data_saved.emit()


# Основной класс приложения PyQt5
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронная загрузка данных")
        
        # Настройка интерфейса
        self.layout = QVBoxLayout()

        # Кнопка для загрузки данных
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # Индикатор выполнения
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress)

        # Метка статуса
        self.status_label = QLabel("Ожидание загрузки данных...")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        # Таймер для периодической загрузки данных
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(10000)

    def load_data(self):
        self.progress.setValue(0)
        self.status_label.setText("Загрузка данных...")

        # Создаем и запускаем DataLoader
        self.loader = DataLoader()
        self.loader.data_loaded.connect(self.on_data_loaded)
        self.loader.start()

    def on_data_loaded(self, data):
        self.status_label.setText("Сохранение данных...")
        self.progress.setValue(50)

        # Создаем и запускаем DataSaver
        self.saver = DataSaver(data)
        self.saver.data_saved.connect(self.on_data_saved)
        self.saver.start()

    def on_data_saved(self):
        self.status_label.setText("Данные успешно сохранены!")
        self.progress.setValue(100)


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
