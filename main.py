import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QWidget, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ingreso de parámetros")
        self.setGeometry(100, 100, 600, 400)  # Aumentamos el tamaño de la ventana

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(20, 20, 560, 300)  # Ajustamos el tamaño de la tabla
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Número de obreros ausentes", "Cantidad de días"])
        self.tableWidget.setRowCount(6)
        for row, value in enumerate(["0", "1", "2", "3", "4", "5 o más"]):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() ^ 2)  # Establece la celda como solo lectura
            self.tableWidget.setItem(row, 0, item)

        # Campos adicionales
        self.dias = self.create_input_field("Número de días a simular")
        self.ventas = self.create_input_field("Valor de ventas diarias")
        self.costo_ventas = self.create_input_field("Costo por ventas diarias")
        self.costo_obrero = self.create_input_field("Costo por obrero diario")
        self.filas_mostrar = self.create_input_field("Filas a mostrar")

        # Botón para guardar los valores
        self.pushButton = QPushButton("Simular", self)
        self.pushButton.setGeometry(250, 340, 100, 30)  # Ajustamos la posición del botón
        self.pushButton.clicked.connect(self.on_click)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addLayout(self.dias[0])
        layout.addLayout(self.ventas[0])
        layout.addLayout(self.costo_ventas[0])
        layout.addLayout(self.costo_obrero[0])
        layout.addLayout(self.filas_mostrar[0])
        layout.addWidget(self.pushButton)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_input_field(self, text):
        layout = QHBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        return layout, input_field

    def on_click(self):
        # Obtiene los valores ingresados por el usuario
        for row in range(6):
            cantidad_dias = self.tableWidget.item(row, 1).text()
            print(f"Fila {row + 1}: {cantidad_dias} días")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())