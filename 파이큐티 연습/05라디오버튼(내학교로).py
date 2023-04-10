from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QRadioButton,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize()
        self.myschoolname = "경희대학교"

    def initialize(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("라디오버튼 연습")
        self.setGeometry(100, 100, 400, 400)

        self.label = QLabel("내가 다니는 대학교는?")
        layout.addWidget(self.label)
        self.label.setFont(QtGui.QFont("Hack", 30))
        self.checked_indicator = QLabel("선택해주세요")
        self.checked_indicator.setFont(QtGui.QFont("Hack", 30))
        layout.addWidget(self.checked_indicator)

        self.radio = QRadioButton("고려대학교")
        self.radio.toggled.connect(self.on_clicked)
        self.radio.setChecked(False)
        layout.addWidget(self.radio)

        self.radio = QRadioButton("경희대학교")
        self.radio.toggled.connect(self.on_clicked)
        self.radio.setChecked(False)
        layout.addWidget(self.radio)

        self.radio = QRadioButton("충남대학교")
        self.radio.toggled.connect(self.on_clicked)
        self.radio.setChecked(False)
        layout.addWidget(self.radio)
        self.show()

    def on_clicked(self):
        radio = self.sender()
        if radio.text() == self.myschoolname:
            self.checked_indicator.setText("정답!")
        else:
            self.checked_indicator.setText("땡!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
