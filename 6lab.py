import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QComboBox, QLineEdit, QWidget, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ данных")
        self.data = None
        
        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание интерфейса
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Кнопка загрузки данных
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)
        
        # Поле статистики
        self.stats_label = QLabel("Здесь будет отображаться статистика данных")
        self.layout.addWidget(self.stats_label)
        
        # Выбор типа графика
        self.chart_type_label = QLabel("Выберите тип графика:")
        self.layout.addWidget(self.chart_type_label)
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Линейный график", "Гистограмма", "Круговая диаграмма"])
        self.layout.addWidget(self.chart_type_combo)
        
        # Кнопка построения графика
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.plot_button)
        
        # Поле для добавления данных
        self.add_data_layout = QHBoxLayout()
        self.add_value_input = QLineEdit()
        self.add_value_input.setPlaceholderText("Введите значение для добавления")
        self.add_data_layout.addWidget(self.add_value_input)
        self.add_value_button = QPushButton("Добавить значение")
        self.add_value_button.clicked.connect(self.add_data_point)
        self.add_data_layout.addWidget(self.add_value_button)
        self.layout.addLayout(self.add_data_layout)
        
        # Поле для графика
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
    
    def load_data(self):
        # Загрузка CSV
        file_path, _ = QFileDialog.getOpenFileName(self, "sample_data.csv", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.update_statistics()
                QMessageBox.information(self, "Успех", "Данные успешно загружены!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")
    
    def update_statistics(self):
        # Обновление статистики
        if self.data is not None:
            stats = self.data.describe(include='all').transpose()
            stats_text = f"Строк: {self.data.shape[0]}, Столбцов: {self.data.shape[1]}\n"
            for col in self.data.columns:
                stats_text += f"{col}: {self.data[col].dtype}\n"
            self.stats_label.setText(stats_text)
    
    def plot_graph(self):
        if self.data is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала загрузите данные!")
            return
        
        graph_type = self.chart_type_combo.currentText()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if graph_type == "Линейный график":
            if "Date" in self.data.columns and "Value1" in self.data.columns:
                self.data.plot(x="Date", y="Value1", ax=ax)
            else:
                QMessageBox.warning(self, "Ошибка", "Нет данных для построения линейного графика.")
        elif graph_type == "Гистограмма":
            if "Date" in self.data.columns and "Value2" in self.data.columns:
                sns.barplot(data=self.data, x="Date", y="Value2", ax=ax)
            else:
                QMessageBox.warning(self, "Ошибка", "Нет данных для построения гистограммы.")
        elif graph_type == "Круговая диаграмма":
            if "Category" in self.data.columns:
                self.data["Category"].value_counts().plot.pie(ax=ax, autopct="%1.1f%%")
            else:
                QMessageBox.warning(self, "Ошибка", "Нет данных для построения круговой диаграммы.")
        
        self.canvas.draw()
    
    def add_data_point(self):
        if self.data is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала загрузите данные!")
            return
        
        value = self.add_value_input.text()
        if value:
            try:
                new_row = pd.DataFrame([[value]], columns=[self.data.columns[0]])
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                self.update_statistics()
                QMessageBox.information(self, "Успех", "Значение успешно добавлено!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить значение: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
