import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QLabel, \
    QLineEdit, QHBoxLayout, QWidget, QMessageBox, QHeaderView


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Montecarlo")
        self.setGeometry(800, 100, 700, 800)  # Aumentamos el tamaño de la ventana

        self.init_main_window()

        # Guarda los valores iniciales de los campos de entrada
        self.initial_values = {
            'dias': '',
            'ventas': '',
            'costo_ventas': '',
            'costo_obrero': '',
            'filas_mostrar': ''
        }

    def init_main_window(self):
        # Primera página
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Número de obreros ausentes", "Cantidad de días"])
        self.tableWidget.setRowCount(6)
        for row, value in enumerate(["0", "1", "2", "3", "4", "5 o más"]):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() ^ 2)  # Establece la celda como solo lectura
            self.tableWidget.setItem(row, 0, item)

        # Ajustar tamaño de las columnas para que se adapten al contenido
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Campos adicionales
        self.dias, self.dias_input = self.create_input_field("Número de días a simular")
        self.ventas, self.ventas_input = self.create_input_field("Valor de ventas diarias")
        self.costo_ventas, self.costo_ventas_input = self.create_input_field("Costo por ventas diarias")
        self.costo_obrero, self.costo_obrero_input = self.create_input_field("Costo por obrero diario")
        self.filas_mostrar, self.filas_mostrar_input = self.create_input_field("Filas a mostrar")

        # Botón para guardar los valores y mostrar la segunda página
        self.pushButton = QPushButton("Simular", self)
        self.pushButton.setGeometry(350, 540, 100, 30)  # Ajustamos la posición del botón
        self.pushButton.clicked.connect(self.show_second_page)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addLayout(self.dias)
        layout.addLayout(self.ventas)
        layout.addLayout(self.costo_ventas)
        layout.addLayout(self.costo_obrero)
        layout.addLayout(self.filas_mostrar)
        layout.addWidget(self.pushButton)

        self.central_widget = QWidget()  # Se agrega la variable central_widget
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def create_input_field(self, text):
        layout = QHBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        return layout, input_field

    def show_second_page(self):
        # Aquí podrías procesar los valores ingresados antes de mostrar la segunda página
        # Por ahora, simplemente pasaremos a la segunda página
        self.init_second_page()

    def init_second_page(self):
        # Segunda página
        self.tableWidgetSecond = QTableWidget(self)
        self.tableWidgetSecond.setColumnCount(2)
        self.tableWidgetSecond.setHorizontalHeaderLabels(["Columna 1", "Columna 2"])
        self.tableWidgetSecond.setRowCount(5)

        self.backButton = QPushButton("Volver", self)
        self.backButton.setGeometry(350, 540, 100, 30)  # Ajustamos la posición del botón
        self.backButton.clicked.connect(self.show_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidgetSecond)
        layout.addWidget(self.backButton)

        second_page_widget = QWidget()
        second_page_widget.setLayout(layout)
        self.setCentralWidget(second_page_widget)

    def show_main_page(self):
        self.init_main_window()

    def reset_input_fields(self):
        # Restablece los campos de entrada borrando su contenido si los objetos QLineEdit aún existen
        self.dias_input.setText('')
        self.ventas_input.setText('')
        self.costo_ventas_input.setText('')
        self.costo_obrero_input.setText('')
        self.filas_mostrar_input.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
