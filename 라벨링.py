from PyQt5.QtWidgets import QWidget, QLabel , QBoxLayout,QVBoxLayout,QApplication, \
    QPushButton, QCheckBox,QRadioButton, QMainWindow ,QFileDialog, QStackedWidget, \
        QMessageBox,QSpinBox,QGroupBox
from PyQt5.QtCore import Qt ,pyqtSignal, pyqtSlot,QThread
from PyQt5 import QtGui , uic
import sys 
from train_model import *
form_class = uic.loadUiType('ui/메인(파일선택).ui')[0]
form_class2 = uic.loadUiType('ui/02모델확인.ui')[0]
form_class3 = uic.loadUiType('ui/03학습과정.ui')[0]
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set()
        self.fname = ''
    def set(self):
        self.file_load_button.clicked.connect(self.fileLoadBtnClick)
        self.next_button.clicked.connect(self.nextPage)
    def fileLoadBtnClick(self):
        self.fname = QFileDialog.getOpenFileName(self)
        self.fname= self.fname[0]
        self.file_name_label.setText(self.fname)
    def nextPage(self):
        if self.fname[-4:]!='xlsx':
            QMessageBox.about(self,'파일 불러오기 오류','라벨링한 엑셀파일을 로드해주세요!')
        else:
            widget.setCurrentIndex(widget.currentIndex()+1)
class SecondPage(QMainWindow,form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set()
        self.fname = WindowClass.fname
    def set(self):
        self.next_button_2.clicked.connect(self.nextPage)
        self.vocab_length_option.setMinimum(50)
        self.vocab_length_option.setMaximum(1000)
        self.vocab_length_option.setValue(500)
        self.idf_log10.setChecked(True)
        self.tf_log10.setChecked(True)
        self.dense01_relu.setChecked(True)
        self.dense02_relu.setChecked(True)
        self.denseout_sigmoid.setChecked(True)
        self.DropoutOption01.setRange(0, 1)
        self.DropoutOption01.setSingleStep(0.1)
        self.DropoutOption02.setRange(0, 1)
        self.DropoutOption02.setSingleStep(0.1)
        self.DropoutOption03.setRange(0, 1)
        self.DropoutOption03.setSingleStep(0.1)
    def nextPage(self):
        print(fname)
        for radio in self.IDF_log.children():
            if radio.isChecked():
                idf_log = radio.text()
        for radio in self.TF_log.children():
            if radio.isChecked():
                tf_log = radio.text()
        vocab_length = int(self.vocab_length_option.value())
        dropout_rate01=round(self.DropoutOption01.value(),2)
        dropout_rate02=round(self.DropoutOption02.value(),2)
        dropout_rate03=round(self.DropoutOption03.value(),2)
        for radio in self.Dense_option01.children():
            if radio.isChecked():
                dense_activation01 = radio.text()
        for radio in self.Dense_option02.children():
            if radio.isChecked():
                dense_activation02 = radio.text()
        for radio in self.Dense_option03.children():
            if radio.isChecked():
                dense_activation03 = radio.text()
        print('11',fname)
        data = read_label_data(fname)
        widget.setCurrentIndex(widget.currentIndex()+1)
class ThirdPage(QMainWindow, form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set()
    def set(self):
        global data14000
        data14000 = read_all_data()
        print(type(data14000))
        self.data = data
        
        self.make_vocab()
    def make_vocab(self):
        self.vocab = mk_vocab(self.data,vocab_length)
        print(self.vocab)
        self.status_make_vocab_label.setText('단어 사전 만들기 (o)')
        self.make_vt()
    def make_vt(self):
        mk_vt(self.data)
        self.status_vectorize_label.setText('데이터 벡터화 하기 (o)')
        self.make_model()
    def make_model(self):
        mk_model()
        self.status_make_model_label.setText('모델 생성 및 설정 (o)')
        print('done')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    myWindow = WindowClass()
    secondPage= SecondPage()
    thirdPage= ThirdPage()
    widget.addWidget(myWindow)
    widget.addWidget(secondPage)
    widget.addWidget(thirdPage)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()
    app.exec_()
# global data 
# global idf_log
# global tf_log
# global vocab_length
# global dropout_rate01
# global dropout_rate02
# global dropout_rate03
# global dense_activation01
# global dense_activation02
# global dense_activation03
# global fname
# fname = ''
# data = ''  
# idf_log='' 
# tf_log='' 
# vocab_length=''
# dropout_rate01=''
# dropout_rate02=''
# dropout_rate03=''
# dense_activation01=''
# dense_activation02=''
# dense_activation03=''