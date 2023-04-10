from PyQt5.QtWidgets import QWidget, QLabel , QApplication , QGridLayout, \
    QVBoxLayout, QCheckBox, QRadioButton, QPushButton, QFileDialog
from PyQt5.QtCore import Qt 
from PyQt5 import QtGui 
import sys 
#-----_#
from collections import Counter 
import pickle 
import openpyxl
import os 
# #-----#
from model import ClassificationModel
filename = ''
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
    def setup(self):
        self.setWindowTitle('라벨링 프로그램')
        self.setGeometry(100,100,200,200)
        layout = QVBoxLayout()
        self.setLayout(layout)
        

        self.label = QLabel('라벨링을 합시다')
        label = self.label
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QtGui.QFont('Hack',30))
        layout.addWidget(self.label)
        
        self.pushButton = QPushButton('작업물 파일 불러오기')
        self.pushButton.clicked.connect(self.pushButtonClicked)
        layout.addWidget(self.pushButton)
        self.show()

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        # global filname
        fname= fname[0]
        classification = ClassificationModel(labelfile=fname,vocab_length=500,label_column_name='당첨자')
        classification.make_model(drop_rate=0)
        classification.compile()
        classification.train(epochs = 10)
        classification.inspect()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())