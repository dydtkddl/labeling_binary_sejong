from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("하이")

        self.label = QLabel("하이하이")
        self.label.setFont(QtGui.QFont("Hack", 30))
        layout = QVBoxLayout()
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(layout)


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec_())
