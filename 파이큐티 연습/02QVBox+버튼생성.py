from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setUp()

    def setUp(self):
        self.label = QLabel("하이")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Hack", 20))
        self.label2 = QLabel("하이2")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QtGui.QFont("Hack", 20))
        self.label3 = QLabel("하이22")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QtGui.QFont("Hack", 20))

        self.button = QPushButton("ddd")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle("타이틀")
        self.setGeometry(200, 200, 200, 200)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
