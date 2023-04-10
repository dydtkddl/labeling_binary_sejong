from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setUP()

    def setUP(self):
        layout = QGridLayout()
        self.setLayout(layout)

        label01 = QLabel("그리드1")
        layout.addWidget(label01, 0, 0)
        label01.setAlignment(Qt.AlignCenter)
        label01.setFont(QtGui.QFont("Hack", 20))

        label02 = QLabel("그리드1")
        layout.addWidget(label02, 0, 1)
        label02.setAlignment(Qt.AlignCenter)
        label02.setFont(QtGui.QFont("Hack", 20))

        label03 = QLabel("그리드1")
        layout.addWidget(label03, 1, 0)
        label03.setAlignment(Qt.AlignCenter)
        label03.setFont(QtGui.QFont("Hack", 20))

        label04 = QLabel("그리드1")
        layout.addWidget(label04, 1, 1)
        label04.setAlignment(Qt.AlignCenter)
        label04.setFont(QtGui.QFont("Hack", 20))

        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("그리드연습")
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
