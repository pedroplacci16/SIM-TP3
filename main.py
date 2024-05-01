import sys
from random import random

from PyQt5.QtCore import Qt
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

        # Inicializar los valores de los campos
        self.dias = 0
        self.ventas = 0
        self.costo_ventas = 0
        self.costo_obrero = 0
        self.filas_mostrar = 0

    def create_input_field(self, text):
        layout = QHBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)

        input_field = QLineEdit()
        layout.addWidget(input_field)

        return layout, input_field

    def show_second_page(self):
        dias_text = self.dias_input.text()
        ventas_text = self.ventas_input.text()
        costo_ventas_text = self.costo_ventas_input.text()
        costo_obrero_text = self.costo_obrero_input.text()
        filas_mostrar_text = self.filas_mostrar_input.text()

        if dias_text.strip() == '' or ventas_text.strip() == '' or costo_ventas_text.strip() == '' \
                or costo_obrero_text.strip() == '' or filas_mostrar_text.strip() == '':
            QMessageBox.warning(self, 'Campos vacíos', 'Por favor, complete todos los campos.')
            return

        dias = int(dias_text)
        ventas = float(ventas_text)
        costo_ventas = float(costo_ventas_text)
        costo_obrero = float(costo_obrero_text)
        filas_mostrar = int(filas_mostrar_text)
        self.init_second_page(dias, ventas, costo_ventas, costo_obrero, filas_mostrar)

    def init_second_page(self, dias, ventas, costo_ventas, costo_obrero, filas_mostrar):
        # Segunda página
        self.tableWidgetSecond = QTableWidget(self)
        self.tableWidgetSecond.setColumnCount(18)
        self.tableWidgetSecond.setHorizontalHeaderLabels(
            ["Reloj", "RND", "AUSENTES", "NÓMINA 21", "NÓMINA 22", "NÓMINA 23",
             "VENTAS 21", "VENTAS 22", "VENTAS 23", "COSTOS DE PRODUCCIÓN 21",
             "COSTOS DE PRODUCCIÓN 22", "COSTOS DE PRODUCCIÓN 23", "SALARIO 21",
             "SALARIO 22", "SALARIO 23", "BENEFICIO 21", "BENEFICIO 22", "BENEFICIO 23"])

        total_dias = sum(int(self.tableWidget.item(row, 1).text()) for row in range(self.tableWidget.rowCount()))

        # Lógica para llenar la tabla
        for i in range(dias):
            # Obtener un valor aleatorio entre 0 y 1 para RND
            rnd = round(random(), 2)

            # Calcular ausentes
            ausentes = self.calcular_ausentes(total_dias, rnd)

            # Calcular NÓMINA
            nomina = [max(0, 21 - ausentes), max(0, 22 - ausentes), max(0, 23 - ausentes)]

            # Calcular VENTAS y COSTOS DE PRODUCCIÓN

            ventas_dia = [0, 0, 0]
            costos_produccion_dia = [0, 0, 0]

            if nomina[0] < 20 and nomina[1] < 20 and nomina[2] < 20:
                ventas_dia = [0, 0, 0]
                costos_produccion_dia = [0, 0, 0]
            elif nomina[0] < 20 and nomina[1] >= 20 and nomina[2] >= 20:
                ventas_dia = [0, ventas, ventas]
                costos_produccion_dia = [0, costo_ventas, costo_ventas]
            elif nomina[0] >= 20 and nomina[1] < 20 and nomina[2] >= 20:
                ventas_dia = [ventas, 0, ventas]
                costos_produccion_dia = [costo_ventas, 0, costo_ventas]
            elif nomina[0] >= 20 and nomina[1] >= 20 and nomina[2] < 20:
                ventas_dia = [ventas, ventas, 0]
                costos_produccion_dia = [costo_ventas, costo_ventas, 0]
            elif nomina[0] < 20 and nomina[1] < 20 and nomina[2] >= 20:
                ventas_dia = [0, 0, ventas]
                costos_produccion_dia = [0, 0, costo_ventas]
            elif nomina[0] < 20 and nomina[1] >= 20 and nomina[2] < 20:
                ventas_dia = [0, ventas, 0]
                costos_produccion_dia = [0, costo_ventas, 0]
            elif nomina[0] >= 20 and nomina[1] < 20 and nomina[2] < 20:
                ventas_dia = [ventas, 0, 0]
                costos_produccion_dia = [costo_ventas, 0, 0]
            else:
                ventas_dia = [ventas, ventas, ventas]
                costos_produccion_dia = [costo_ventas, costo_ventas, costo_ventas]

            # Calcular SALARIO
            salario = [x * costo_obrero for x in [21, 22, 23]]

            beneficio = [0, 0, 0]  # Vector de beneficios inicializado con tres ceros
            beneficio_acumulado = [0, 0, 0]  # Inicializamos beneficio_acumulado con los mismos valores que beneficio


            # Calcular beneficio para cada columna

            for j in range(3):  # Iteración sobre las columnas
                if i == 0:
                    # Si es la primera fila, simplemente calculamos el beneficio
                    beneficio[j] = ventas_dia[j] - costos_produccion_dia[j] - salario[j]
                else:
                    # Si no es la primera fila, sumamos el beneficio de la fila actual al beneficio acumulado anterior
                    beneficio[j] = (ventas_dia[j] - costos_produccion_dia[j] - salario[j])


            # Insertar fila en la tabla
            self.tableWidgetSecond.insertRow(i)
            self.tableWidgetSecond.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.tableWidgetSecond.setItem(i, 1, QTableWidgetItem(str(rnd)))
            self.tableWidgetSecond.setItem(i, 2, QTableWidgetItem(str(ausentes)))

            # Llenar la tabla
            for j in range(3, 18):
                if j < 6:
                    self.tableWidgetSecond.setItem(i, j, QTableWidgetItem(str(nomina[j - 3])))
                elif j < 9:
                    self.tableWidgetSecond.setItem(i, j, QTableWidgetItem(str(ventas_dia[j - 6])))
                elif j < 12:
                    self.tableWidgetSecond.setItem(i, j, QTableWidgetItem(str(costos_produccion_dia[j - 9])))
                elif j < 15:
                    self.tableWidgetSecond.setItem(i, j, QTableWidgetItem(str(salario[j - 12])))
                else:
                    self.tableWidgetSecond.setItem(i, j, QTableWidgetItem(str(beneficio[j - 15])))

        self.backButton = QPushButton("Volver", self)
        self.backButton.setGeometry(350, 540, 100, 30)  # Ajustamos la posición del botón
        self.backButton.clicked.connect(self.show_main_page)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidgetSecond)
        layout.addWidget(self.backButton)

        second_page_widget = QWidget()
        second_page_widget.setLayout(layout)

        self.setCentralWidget(second_page_widget)

    def calcular_ausentes(self, total_dias, rnd):
        limites_inferiores = [0]
        numeros_ausentes = [0, 1, 2, 3, 4, 5]

        for row in range(self.tableWidget.rowCount() - 1):
            dias = int(self.tableWidget.item(row, 1).text())
            if total_dias == 0:
                limites_inferiores.append(limites_inferiores[-1])
            else:
                proporciones = dias / total_dias

                limites_inferiores.append(limites_inferiores[-1] + round(proporciones, 2))

        ausentes = self.buscar(rnd, limites_inferiores, numeros_ausentes)

        return ausentes

    def buscar(self, rnd, limites_inf, numeros_ausentes):
        for i, limite_inf in enumerate(limites_inf):
            if rnd < limite_inf:
                return numeros_ausentes[i - 1]
        return numeros_ausentes[-1]

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
