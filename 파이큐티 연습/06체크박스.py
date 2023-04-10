from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QCheckBox,
    QRadioButton,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setWindowTitle("체크박스연습")
        self.setGeometry(100, 100, 200, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("체크박스를 만들어 보아요(동물)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.label)

        self.indicator = QLabel("동물을 선택해주세요")
        self.indicator.setAlignment(Qt.AlignCenter)
        self.indicator.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.indicator)

        self.check01 = QCheckBox("사자")
        self.check01.setChecked(False)
        self.check01.toggled.connect(self.check)
        self.check01.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.check01)

        self.check02 = QCheckBox("호랑이")
        self.check02.setChecked(False)
        self.check02.toggled.connect(self.check)
        self.check02.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.check02)

        self.check03 = QCheckBox("늑대")
        self.check03.setChecked(False)
        self.check03.toggled.connect(self.check)
        self.check03.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.check03)

        self.check04 = QCheckBox("하이에나")
        self.check04.setChecked(False)
        self.check04.toggled.connect(self.check)
        self.check04.setFont(QtGui.QFont("Hack", 20))
        layout.addWidget(self.check04)

        self.show()

    def check(self):
        checked = []
        items = ""
        if self.check01.isChecked():
            checked += [self.check01.text()]
        else:
            if self.check01.text() in checked:
                checked.remove(self.check01.text())
        if self.check02.isChecked():
            checked += [self.check02.text()]
        else:
            if self.check02.text() in checked:
                checked.remove(self.check02.text())
        if self.check03.isChecked():
            checked += [self.check03.text()]
        else:
            if self.check03.text() in checked:
                checked.remove(self.check03.text())
        if self.check04.isChecked():
            checked += [self.check04.text()]
        else:
            if self.check04.text() in checked:
                checked.remove(self.check04.text())
        items = "_".join(checked)
        self.indicator.setText(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
