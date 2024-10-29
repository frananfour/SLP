import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QTableView, 
                             QMessageBox, QDialog, QLabel, QFormLayout, QDialogButtonBox)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("Database App")
        self.resize(600, 400)
        
        # Основной виджет
        widget = QWidget()
        self.setCentralWidget(widget)
        
        # Основной layout
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Поле поиска
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск по заголовку")
        self.search_field.textChanged.connect(self.search)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Обновить")
        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить")
        
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_record)
        self.delete_button.clicked.connect(self.delete_record)
        
        btn_layout.addWidget(self.refresh_button)
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.delete_button)
        
        # Таблица для отображения данных
        self.table_view = QTableView()
        
        # Подключение к базе данных
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.load_data()
        
        # Добавление элементов в основной layout
        layout.addWidget(self.search_field)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_view)

    def load_data(self):
        # Загрузка данных из базы в таблицу
        self.model = QSqlTableModel(self)
        self.model.setTable("posts")
        self.model.select()
        
        # Отображение данных в QTableView
        self.table_view.setModel(self.model)
    
    def search(self):
        # Поиск по заголовку
        filter_str = self.search_field.text()
        self.model.setFilter(f"title LIKE '%{filter_str}%'")
        self.model.select()
    
    def add_record(self):
        # Открытие диалога для добавления новой записи
        dialog = AddRecordDialog(self)
        if dialog.exec():
            user_id, title, body = dialog.get_data()
            self.cursor.execute("INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)", (user_id, title, body))
            self.conn.commit()
            self.load_data()

    def delete_record(self):
        # Удаление выбранной записи
        selected_row = self.table_view.currentIndex().row()
        if selected_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return
        
        reply = QMessageBox.question(self, "Удаление", "Вы уверены, что хотите удалить выбранную запись?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.model.removeRow(selected_row)
            self.model.submitAll()
            self.load_data()

# Диалог для добавления новой записи
class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Добавить запись")
        self.setLayout(QFormLayout())
        
        # Поля для ввода данных
        self.user_id_field = QLineEdit()
        self.title_field = QLineEdit()
        self.body_field = QLineEdit()
        
        # Кнопки для подтверждения или отмены добавления
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление полей и кнопок в layout
        self.layout().addRow("User ID:", self.user_id_field)
        self.layout().addRow("Title:", self.title_field)
        self.layout().addRow("Body:", self.body_field)
        self.layout().addWidget(button_box)
        
    def get_data(self):
        # Получение данных из полей
        return int(self.user_id_field.text()), self.title_field.text(), self.body_field.text()

# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
