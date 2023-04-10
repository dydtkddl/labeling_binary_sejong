from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setUp()
        self.count = 0

    def setUp(self):
        layout = QGridLayout()
        self.setLayout(layout)

        self.label = QLabel("카운트")
        label = self.label
        layout.addWidget(label, 0, 0)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QtGui.QFont("Hack", 20))
        self.label1 = QLabel("카운트")
        label1 = self.label1
        layout.addWidget(label1, 0, 1)
        label1.setAlignment(Qt.AlignCenter)
        label1.setFont(QtGui.QFont("Hack", 20))

        button_sub = QPushButton("빼기 1")
        layout.addWidget(button_sub, 1, 0)
        button_sub.clicked.connect(self.button_sub)
        button_sub.setFont(QtGui.QFont("Hack", 20))
        button = QPushButton("더하기 1")
        button.clicked.connect(self.button)
        layout.addWidget(button, 1, 1)
        button.setFont(QtGui.QFont("Hack", 20))

        self.setWindowTitle("버튼이벤트 처리")
        self.setGeometry(100, 100, 500, 500)
        self.show()

    def button_sub(self):
        print("버튼 클릭됌(sub)", self.count)
        self.count -= 1
        self.label1.setText("Count" + str(self.count))

    def button(self):
        print("버튼 클릭됌", self.count)
        self.count += 1
        self.label1.setText("Count" + str(self.count))


import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
