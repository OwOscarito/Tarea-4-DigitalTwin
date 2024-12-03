import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import use
use("Qt5Agg")
import matplotlib.pyplot as plt

import logging
import receiver
import threading

MAX_TRIES = 3

class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.acc_data = [0, 0, 0]
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.canvas = FigureCanvas(self.fig)
        self.quiver = self.ax.quiver(*self.get_arrow())
        self.ax.set(xlim=[-1.5, 1.5], ylim=[-1.5, 1.5], zlim=[-1.5, 1.5])

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.show()

    def get_arrow(self) -> None:
        u = self.acc_data[0]
        v = self.acc_data[1]
        w = self.acc_data[2]
        return 0, 0, 0, -u, v, -w

    def update(self, data: tuple[float, float, float]) -> None:
        self.acc_data = data
        self.quiver.remove()
        self.quiver = self.ax.quiver(*self.get_arrow())
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #Ajustes de parametros iniciales
        self.title = "Digital Twin BMI 270"
        self.left = 50
        self.top = 50
        self.width = 700
        self.height = 800
        self.connected = False
        self.thread = None
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Boton para cambiar ventana
        self.connect_button = QPushButton("Conectar", self)
        # Label para mostrar el estado actual
        self.connect_button.clicked.connect(self.connection_manager)

        # Visualizador
        self.visualizer = Visualizer()

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.connect_button)

        # Set main_layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.visualizer)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        receiver.init_receiver()

    def reader_thread(self) -> None:
        while self.connected:
            data = receiver.receive_acc_data()
            if data:
                self.visualizer.update(data)

    def start_reader(self) -> bool:
        if receiver.test_conn():  # noqa: SIM102
            if receiver.start_message():
                self.connect_button.setText("Desconectar")
                self.connected = True
                self.thread = threading.Thread(target=self.reader_thread)
                self.thread.start()
                return True
        logging.error("Couldn't start reading")
        return False

    def stop_reader(self) -> None:
        self.connected = False
        if self.thread:
            self.thread.join()
            self.thread = None
        receiver.stop_message()
        self.connect_button.setText("Conectar")


    @pyqtSlot()
    def connection_manager(self) -> None:
        if self.connected:
            self.stop_reader()
            return

        if self.start_reader():
            return
        self.stop_reader()
        self.start_reader()

if __name__ == "__main__":
    LOGGING_FORMAT = "%(levelname)s - <%(funcName)s>: %(message)s"
    logging.basicConfig(format=LOGGING_FORMAT,
                        style="%",
                        level=logging.DEBUG)
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
