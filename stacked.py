from PyQt5.QtWidgets import QWidget, QLabel , QBoxLayout,QVBoxLayout,QApplication, \
    QPushButton, QCheckBox,QRadioButton, QMainWindow ,QFileDialog, QStackedWidget, \
        QMessageBox,QSpinBox,QGroupBox,QDialog,QStackedWidget,QFrame,QHBoxLayout,QTableWidgetItem,\
            QTableWidget,QHeaderView   ,QInputDialog
from PyQt5.QtCore import Qt ,pyqtSignal, pyqtSlot,QThread
from PyQt5 import QtGui , uic
import sys 
import os 
import openpyxl
from train_model import *
import pandas as pd
import os
import tensorflow as tf
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
form_class = resource_path('ui/메인(파일선택).ui')
form_class = uic.loadUiType(form_class)[0]
form_class2 = resource_path('ui/02모델확인.ui')
form_class2 = uic.loadUiType(form_class2)[0]
form_class3 = resource_path('ui/03학습과정.ui')
form_class3 = uic.loadUiType(form_class3)[0]
form_class4 = resource_path('ui/04검수.ui')
form_class4 = uic.loadUiType(form_class4)[0]
form_class5 = resource_path('ui/05예측.ui')
form_class5 = uic.loadUiType(form_class5)[0]
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.next_button.clicked.connect(self.next_btn)
        self.file_load_button.clicked.connect(self.fileLoadBtnClick)
    def fileLoadBtnClick(self):
        self.fname = QFileDialog.getOpenFileName(self)
        self.fname= self.fname[0]
        self.file_name_label.setText(self.fname)
    def next_btn(self):
        if self.fname[-4:]!='xlsx':
            QMessageBox.about(self,'파일 불러오기 오류','라벨링한 엑셀파일을 로드해주세요!')
        else:
            self.hide()
            self.second = SecondWindow(self.fname)
            self.second.exec()
            self.show()
class SecondWindow(QDialog,QWidget,form_class2):
    def __init__(self,fname):
        QDialog.__init__(self)
        self.fname = fname
        print(self.fname)
        self.initUi()
        self.show()
    def initUi(self):
        self.setupUi(self)
        self.next_button_2.clicked.connect(self.next_btn)
        self.load_model_btn.clicked.connect(self.load_model)
        self.vocab_length_option.setMinimum(50)
        self.vocab_length_option.setMaximum(1000)
        self.vocab_length_option.setValue(500)
        self.epochs.setMinimum(1)
        self.epochs.setMaximum(1000)
        self.epochs.setValue(10)

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
    def load_model(self):
        self.model = QFileDialog.getOpenFileName(self)
        self.model= self.model[0]
        if self.model[-2:]!='h5':
            a = QMessageBox.about(self,'파일오류','올바른 파일을 입력해주세요')
        else:
            self.model = tf.keras.models.load_model(self.model)
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
            epochs = int(self.epochs.value())
            for radio in self.Dense_option01.children():
                if radio.isChecked():
                    dense_activation01 = radio.text()
            for radio in self.Dense_option02.children():
                if radio.isChecked():
                    dense_activation02 = radio.text()
            for radio in self.Dense_option03.children():
                if radio.isChecked():
                    dense_activation03 = radio.text()
            self.hide()
            self.second = ThirdWindow(self.fname,idf_log,tf_log,vocab_length,dropout_rate01,
            dropout_rate02,dropout_rate03, dense_activation01,dense_activation02,dense_activation03,epochs,self.model)
            self.second.exec()
    def next_btn(self):
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
        epochs = int(self.epochs.value())
        for radio in self.Dense_option01.children():
            if radio.isChecked():
                dense_activation01 = radio.text()
        for radio in self.Dense_option02.children():
            if radio.isChecked():
                dense_activation02 = radio.text()
        for radio in self.Dense_option03.children():
            if radio.isChecked():
                dense_activation03 = radio.text()
        self.hide()
        self.second = ThirdWindow(self.fname,idf_log,tf_log,vocab_length,dropout_rate01,
        dropout_rate02,dropout_rate03, dense_activation01,dense_activation02,dense_activation03,epochs,'no_model')
        self.second.exec()
class ThirdWindow(QDialog, QWidget, form_class3):
    def __init__(self,fname,idf,tf,vl,dr1,dr2,dr3,da1,da2,da3,epochs,model):
        super(ThirdWindow,self).__init__()
        self.idf_log=idf 
        self.tf_log=tf
        self.vocab_length = vl 
        self.dropout_rate01 = dr1 
        self.dropout_rate02 = dr2 
        self.dropout_rate03 = dr3
        self.dense_activation01 = da1
        self.dense_activation02 = da2
        self.dense_activation03 = da3
        self.fname = fname
        self.epochs = epochs
        self.model = model
        self.setupUi(self)
        self.show()
        self.initUi()
        self.show()
    def initUi(self):
        self.data14000 = read_all_data()
        self.data = read_label_data(filename=self.fname,label_name='label')
        self.re_train_button.clicked.connect(self.retrain)
        self.go_to_inspect_button.clicked.connect(self.inspect)
        self.make_vocab()
    def retrain(self):
        self.hide()
        self.second = SecondWindow(fname=self.fname)
        self.second.exec()
    def make_vocab(self):
        if self.model == 'no_model':
            self.vocab = mk_vocab(self.data,self.vocab_length)
            self.vocab = [x for x,y in self.vocab]
        else:
            self.vocab = mk_vocab(self.data,self.model.input_shape[1])
            self.vocab = [x for x,y in self.vocab]
        with open('%s_vocab'%self.fname[:-5],'wb') as f:
            pickle.dump(self.vocab, f)
        # self.status_make_vocab_label.setText('단어 사전 만들기 (o)')
        self.make_vt()
    def make_vt(self):
        if self.model != 'no_model':
            self.vocab_length = self.model.input_shape[1]            
        self.tf_idf,self.idf = mk_vt(self.data,self.tf_log,self.idf_log,self.vocab_length,self.vocab,len(self.data14000))
        self.target = self.data.loc[:,['label']]
        self.train_data, self.test_data, self.train_target, self.test_target = split_data(self.tf_idf, self.target)
        with open('%s_idf'%self.fname[:-5],'wb') as f:
            pickle.dump(self.idf, f)
        # self.status_vectorize_label.setText('데이터 벡터화 하기 (o)')
        if self.model == 'no_model':
            self.make_model()
        else:
            self.ev = self.model.evaluate(self.test_data,self.test_target)
            self.test_model()
    def make_model(self):
        print('모델 만들기끝')
        self.model = mk_model(self.dropout_rate01,self.dropout_rate02,self.dropout_rate03,
                 self.dense_activation01,self.dense_activation02,self.dense_activation03,self.vocab_length)
        print('모델 만들기끝')
        # self.status_make_model_label.setText('모델 생성 및 설정 (o)')
        self.train_model()
    def train_model(self):
        self.model ,self.history= train_model(self.model, self.tf_idf, self.target,self.epochs,self.train_data, self.test_data, self.train_target, self.test_target)
        self.history = self.history.history
        print(self.history)
        self.test_model()
    def test_model(self):
        self.pre_list = []
        for pre in test_model(self.model,self.tf_idf):
            if pre[0]>0.5:
                self.pre_list.append(1)
            else:
                self.pre_list.append(0)
    def inspect(self):
        self.hide()
        self.second = FourthWindow(self.data, self.pre_list,self.data14000,self.idf_log,self.tf_log, self.vocab_length,self.vocab,self.model)
        self.second.exec()
class FourthWindow(QDialog, QWidget, form_class4):
    def __init__(self, data, pre_list,data14000,idf_log, tf_log,vocab_length, vocab,model):
        super(FourthWindow,self).__init__()
        self.data = data
        self.pre_list = pre_list
        self.data14000 = data14000
        self.idf_log = idf_log
        self.tf_log = tf_log
        self.vocab_length = vocab_length
        self.vocab = vocab
        self.model = model
        self.column_headers = ['Index','title','check','real','pre']
        self.checked = np.zeros((len(self.pre_list),))
        self.setupUi(self)
        self.initUi()
        self.show()
    def initUi(self):
        self.titles = self.data.loc[:,'title']
        self.real = self.data.loc[:, 'label']
        self.compare()
        self.save_model.clicked.connect(self.model_save)
        self.check_all.clicked.connect(lambda :self.check_all_())
        self.insert(mode='oo',first=1)
        self.newlabel_save.clicked.connect(self.save_newfile)
        self.retrain_btn.clicked.connect(self.retrain)
        self.filter_input_btn.clicked.connect(self.search_filter)
        self.next_btn.clicked.connect(self.next)
        self.oo_btn.clicked.connect(lambda :self.insert(mode='oo',first=0))
        self.oz_btn.clicked.connect(lambda :self.insert(mode='oz',first=0))
        self.zo_btn.clicked.connect(lambda :self.insert(mode='zo',first=0))
        self.zz_btn.clicked.connect(lambda :self.insert(mode='zz',first=0))
    def check_all_(self):
        rows = self.oo_table.rowCount()
        print(rows)
        if self.check_all.isChecked():
            for i in range(rows):
                self.oo_table.cellWidget(i,2).setChecked(True)
        else:
            for i in range(rows):
                self.oo_table.cellWidget(i,2).setChecked(False)
    def model_save(self):
        if os.path.isdir('saved_model')==False:
            os.mkdir('saved_model')
        os.chdir('saved_model')
        text, ok = QInputDialog.getText(self, '저장파일이름', '저장할 파일 이름(h5):')
        file_c = 1
        while True:
            if os.path.isfile('%s_%s.h5'%(text,file_c)) == False:
                break
            else:
                file_c+=1
        
        self.save_full_modelname = 'saved_model/%s_%s.xlsx'%(text,file_c)
        self.save_modelname = '%s_%s.h5'%(text,file_c)
        self.model.save(self.save_modelname)
        os.chdir('../')            
        print('저장완료')
    def next(self):
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        self.hide()
        self.second = FiveWindow(self.data, self.data14000,self.idf_log,self.tf_log,self.vocab_length,self.vocab,self.model,self.checked)
        self.second.exec()
    def compare(self):
        self.one_one = []
        self.one_ze = []
        self.ze_one = []
        self.ze_ze = []
        index = 0
        for real, pre,title in zip(self.real, self.pre_list,self.titles):
            if real ==1:
                if pre ==1:
                    self.one_one.append([real,pre,title, index])
                else:
                    self.one_ze.append([real,pre,title, index])
            else:
                if pre ==1:
                    self.ze_one.append([real,pre,title, index])
                else:
                    self.ze_ze.append([real,pre,title, index])
            index+=1
        self.oo_table.setColumnCount(5)
        self.oo_table.setHorizontalHeaderLabels(self.column_headers)
        column = self.oo_table.horizontalHeader()
        self.oo_table.setRowCount(10)

        column.resizeSection(0,50)
        column.resizeSection(1,720)
        column.resizeSection(2,70)
        column.resizeSection(3,30)
        column.resizeSection(4,30)
    def search_filter(self):
        text = self.filter_input.text()
        filter_words = text.split('&')
        filter =[]
        for word in filter_words:
            filter.append(word.split('|'))
        rowcount = self.oo_table.rowCount()
        i_list = []
        for i in range(0, rowcount):
            tit = self.oo_table.item(i,1).text()
            indx = self.oo_table.item(i,0).text()
            li = []
            for w_l in filter:
                cou =0
                for w in w_l:
                    if re.search(w, tit)!=None:
                        cou+=1
                li.append(cou)
            if 0 not in li:
                i_list.append(int(indx))
        filtered_data =[]
        ix = 0
        for real, pre,title in zip(self.real, self.pre_list,self.titles):
            if ix in i_list:
                filtered_data.append([real,pre,title,ix])
            ix+=1
        self.oo_table.setRowCount(len(i_list))
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        self.dict_ = {}
        c=0
        for real, pre, title,index in filtered_data:
            self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
            self.oo_table.setItem(c,1,QTableWidgetItem(title))
            self.dict_[index] = QCheckBox()
            if self.checked[index]==1:
                self.dict_[index].setChecked(True)
            self.oo_table.setCellWidget(c,2,self.dict_[index])
            self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
            self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
            c+=1
        self.filter_count.setText('%s건 조회'%c)
    def insert(self, mode,first):
        if mode == 'oo' and first==1:
            print('first')
            c=0
            self.oo_table.setRowCount(len(self.one_one))
            self.dict_ = {}
            for real, pre, title,index in self.one_one:
                self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.oo_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                self.oo_table.setCellWidget(c,2,self.dict_[index])
                self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
                self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
        elif mode == 'oo' and first == 0:
            self.check_all.setChecked(False)
            self.oo_table.setRowCount(len(self.one_one))
            c=0
            for index, value in self.dict_.items():
                if value.isChecked():
                    self.checked[index]=1
            self.dict_ = {}
            for real, pre, title,index in self.one_one:
                self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.oo_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                if self.checked[index]==1:
                    self.dict_[index].setChecked(True)
                self.oo_table.setCellWidget(c,2,self.dict_[index])
                self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
                self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
            self.filter_input.clear()
            self.filter_count.setText('')
        elif mode=='oz':
            self.check_all.setChecked(False)
            self.oo_table.setRowCount(len(self.one_ze))
            for index, value in self.dict_.items():
                if value.isChecked():
                    self.checked[index]=1
            self.dict_ = {}
            c=0
            for real, pre, title,index in self.one_ze:
                self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.oo_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                if self.checked[index]==1:
                    self.dict_[index].setChecked(True)
                self.oo_table.setCellWidget(c,2,self.dict_[index])
                self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
                self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
            self.filter_input.clear()
            self.filter_count.setText('')

        elif mode=='zo':
            self.check_all.setChecked(False)
            self.oo_table.setRowCount(len(self.ze_one))
            for index, value in self.dict_.items():
                if value.isChecked():
                    self.checked[index]=1
            self.dict_ = {}
            c=0
            for real, pre, title,index in self.ze_one:
                self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.oo_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                if self.checked[index]==1:
                    self.dict_[index].setChecked(True)
                self.oo_table.setCellWidget(c,2,self.dict_[index])
                self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
                self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
            self.filter_count.setText('')
            self.filter_input.clear()
        elif mode=='zz':
            self.check_all.setChecked(False)
            self.oo_table.setRowCount(len(self.ze_ze))
            for index, value in self.dict_.items():
                if value.isChecked():
                    self.checked[index]=1
            self.dict_ = {}
            c=0
            for real, pre, title,index in self.ze_ze:
                self.oo_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.oo_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                if self.checked[index]==1:
                    self.dict_[index].setChecked(True)
                self.oo_table.setCellWidget(c,2,self.dict_[index])
                self.oo_table.setItem(c,3,QTableWidgetItem(str(real)))
                self.oo_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
            self.filter_count.setText('')
            self.filter_input.clear()
    def save_newfile(self):
        print('clicked')
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        content_list = []
        title_list = []
        noun_list = []
        label_list = []
        for ch,content,title,noun,label in zip(self.checked,self.data.loc[:,'content'],self.data.loc[:,'title'],self.data.loc[:,'nouns'],self.data.loc[:,'label']):
            content_list.append(content)
            title_list.append(title)
            noun_list.append(noun)
            if ch != 1:
                label_list.append(label)
            else:
                if label ==1:
                    label_list.append(0)
                else:
                    label_list.append(1)
        
        new_file = pd.DataFrame({'content':content_list,'title':title_list,'nouns':noun_list,'label':label_list})
        if os.path.isdir('new_labelling_file')==False:
            os.mkdir('new_labelling_file')
        os.chdir('new_labelling_file')
        text, ok = QInputDialog.getText(self, '저장파일이름', '저장할 파일 이름:')
        file_c = 1
        while True:
            if os.path.isfile('new_labelling_file_%s_%s.xlsx'%(text,file_c)) == False:
                break
            else:
                file_c+=1
        
        self.new_full_name = 'new_labelling_file/new_labelling_file_%s_%s.xlsx'%(text,file_c)
        self.new_file_name = 'new_labelling_file_%s_%s.xlsx'%(text,file_c)
        new_file.to_excel(self.new_file_name)
        os.chdir('../')            
        print('저장완료')
    def retrain(self):
        self.save_newfile()
        self.hide()
        self.second = SecondWindow(fname = self.new_full_name)
        self.second.exec()
class FiveWindow(QDialog, QWidget, form_class5):
    def __init__(self,data,data14000,idf_log, tf_log, vocab_length , vocab,model,checked):
        super(FiveWindow,self).__init__()
        self.setupUi(self)
        self.data = data
        self.data14000 =data14000
        self.idf_log = idf_log
        self.tf_log = tf_log
        self.before_checked = checked
        self.vocab_length  = vocab_length 
        self.vocab = vocab
        self.model = model
        self.page = 1
        self.dict_ = {}
        self.ch_dict_ = {}
        self.one_zero_data = (1,2,3)
        self.predict_table.setColumnCount(5)
        self.column_headers = ['Index','title','check','change','pre']
        self.predict_table.setHorizontalHeaderLabels(self.column_headers)
        column = self.predict_table.horizontalHeader()
        column.resizeSection(0,50)
        column.resizeSection(1,620)
        column.resizeSection(2,70)
        column.resizeSection(3,70)
        column.resizeSection(4,30)
        self.initUi()
        self.show()

    def initUi(self):
        self.pre_1_btn.clicked.connect(lambda:self.insert(mode='1',first='0'))
        self.pre_0_btn.clicked.connect(lambda:self.insert(mode='0',first='0'))
        self.before_page.clicked.connect(lambda :self.change_page(mode='before'))
        self.next_page.clicked.connect(lambda:self.change_page(mode='next'))
        self.save_model.clicked.connect(self.model_save)
        self.filter_btn.clicked.connect(self.filter)
        self.retrain_btn.clicked.connect(self.retrain)
        self.save_file_btn.clicked.connect(self.save_file)
        self.left_all.clicked.connect(lambda :self.check_all(mode='left'))
        self.right_all.clicked.connect(lambda :self.check_all(mode='right'))
        self.show()
        self.get_pre_list()
        self.checked = np.zeros((len(self.pre_list),))
        self.is_change = np.zeros((len(self.pre_list),))
        
        self.insert(mode='1',first='1')
    def get_pre_list(self):
        self.pre_list,self.data_merged = predict(self.model,self.data14000,self.data, self.tf_log,self.idf_log,self.vocab_length,self.vocab)
        self.one = []
        self.zero = []
        index = 0
        for pre, title in zip(self.pre_list,self.data_merged.loc[:,'title']):
            if pre<0.5:
                self.zero.append([index, title,0 ])
            else:
                self.one.append([index, title,1 ])
            index +=1
    def check_all(self,mode):
        rows = self.predict_table.rowCount()
        if mode == 'left':
            if self.left_all.isChecked():
                for i in range(rows):
                    self.predict_table.cellWidget(i,2).setChecked(True)
            else:
                for i in range(rows):
                    self.predict_table.cellWidget(i,2).setChecked(False)
        else:
            if self.right_all.isChecked():
                for i in range(rows):
                    self.predict_table.cellWidget(i,3).setChecked(True)
            else:
                for i in range(rows):
                    self.predict_table.cellWidget(i,3).setChecked(False)
    def change_page(self,mode):
        self.row_count = len(self.one_zero_data)
        self.left_all.setChecked(False)
        self.right_all.setChecked(False)
        if mode == 'before':
            if self.page !=1:
                self.page -=1
        else:
            if self.page !=(int(self.row_count)//30)+1:
                self.page+=1
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        for index, value in self.ch_dict_.items():
            if value.isChecked():
                self.is_change[index]=1
        self.predict_table.setRowCount(30)
        self.dict_ = {}
        self.ch_dict_={}
        start = 30*(self.page-1)
        if self.page ==(int(self.row_count)//30)+1:
            last = self.row_count
        else:
            last = 30*(self.page)
        c=0
        print(len(self.one_zero_data))

        for index,title,pre in self.one_zero_data[start:last]:
            self.predict_table.setItem(c,0,QTableWidgetItem(str(index)))
            self.predict_table.setItem(c,1,QTableWidgetItem(title))
            self.dict_[index] = QCheckBox()
            if self.checked[index]==1:
                self.dict_[index].setChecked(True)
            self.predict_table.setCellWidget(c,2,self.dict_[index])
            self.ch_dict_[index] = QCheckBox()
            if self.is_change[index]==1:
                self.ch_dict_[index].setChecked(True)
            self.predict_table.setCellWidget(c,3,self.ch_dict_[index])
            self.predict_table.setItem(c,4,QTableWidgetItem(str(pre)))
            c+=1
        self.page_num.setText('%s 페이지'%self.page)
    def insert(self,mode,first):
        self.page_num.setText('1 페이지')
        if first =='1':
            self.one_zero_data = self.one
            print('first')
            c=0
            self.page =1
            
            self.predict_table.setRowCount(30)
            if len(self.one)<30:
                self.predict_table.setRowCount(len(self.one))

            self.dict_ = {}
            self.ch_dict_ ={}
            for index,title,pre in self.one:
                self.predict_table.setItem(c,0,QTableWidgetItem(str(index)))
                self.predict_table.setItem(c,1,QTableWidgetItem(title))
                self.dict_[index] = QCheckBox()
                self.predict_table.setCellWidget(c,2,self.dict_[index])
                self.ch_dict_[index] = QCheckBox()
                self.predict_table.setCellWidget(c,3,self.ch_dict_[index])
                self.predict_table.setItem(c,4,QTableWidgetItem(str(pre)))
                c+=1
        else:
            if mode =='1':
                self.one_zero_data = self.one

                c=0
                self.page = 1
                for index, value in self.dict_.items():
                    if value.isChecked():
                        self.checked[index]=1
                for index, value in self.ch_dict_.items():
                    if value.isChecked():
                        self.is_change[index]=1
                self.predict_table.setRowCount(30)
                if len(self.one)<30:
                    self.predict_table.setRowCount(len(self.one))
                self.dict_ = {}
                self.ch_dict_={}
                for index,title,pre in self.one[:30]:
                    self.predict_table.setItem(c,0,QTableWidgetItem(str(index)))
                    self.predict_table.setItem(c,1,QTableWidgetItem(title))
                    self.dict_[index] = QCheckBox()
                    if self.checked[index]==1:
                        self.dict_[index].setChecked(True)
                    self.predict_table.setCellWidget(c,2,self.dict_[index])
                    self.ch_dict_[index] = QCheckBox()
                    if self.is_change[index]==1:
                        self.ch_dict_[index].setChecked(True)
                    self.predict_table.setCellWidget(c,3,self.ch_dict_[index])
                    self.predict_table.setItem(c,4,QTableWidgetItem(str(pre)))
                    c+=1
                
            elif mode=='0':
                c=0 
                self.one_zero_data = self.zero
                self.page = 1
                for (index, value),(index2, value2) in zip(self.dict_.items(),self.ch_dict_.items()):
                    if value.isChecked():
                        self.checked[index]=1
                # for index, value in self.ch_dict_.items():
                    if value2.isChecked():
                        self.is_change[index2]=1
                self.predict_table.setRowCount(30)
                if len(self.zero)<30:
                    self.predict_table.setRowCount(len(self.zero))
                self.dict_ = {}
                self.ch_dict_={}
                for index,title,pre in self.zero[:30]:
                    print(1)
                    self.predict_table.setItem(c,0,QTableWidgetItem(str(index)))
                    self.predict_table.setItem(c,1,QTableWidgetItem(title))
                    self.dict_[index] = QCheckBox()
                    if self.checked[index]==1:
                        self.dict_[index].setChecked(True)
                    self.predict_table.setCellWidget(c,2,self.dict_[index])
                    self.ch_dict_[index] = QCheckBox()
                    if self.is_change[index]==1:
                        self.ch_dict_[index].setChecked(True)
                    self.predict_table.setCellWidget(c,3,self.ch_dict_[index])
                    self.predict_table.setItem(c,4,QTableWidgetItem(str(pre)))
                    c+=1
    def filter(self):
        text = self.filter_input.text()
        filter_words = text.split('&')
        filter =[]
        for word in filter_words:
            filter.append(word.split('|'))
        rowcount = len(self.one_zero_data)
        i_list = []
        for i in range(0, rowcount):
            tit = self.one_zero_data[i][1]
            indx = self.one_zero_data[i][0]
            li = []
            for w_l in filter:
                cou =0
                for w in w_l:
                    if re.search(w, tit)!=None:
                        cou+=1
                li.append(cou)
            if 0 not in li:
                i_list.append(int(indx))
        filtered_data =[]
        ix = 0
        for pre,title in zip(self.pre_list,self.data_merged['title']):
            if ix in i_list:
                if pre<0.5:
                    filtered_data.append([0,title,ix])
                else:
                    filtered_data.append([1,title,ix])
            ix+=1
        self.predict_table.setRowCount(len(i_list))
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        self.dict_ = {}
        for index, value in self.ch_dict_.items():
            if value.isChecked():
                self.is_change[index]=1
        self.ch_dict_ = {}
        c=0
        for pre,title,index in filtered_data:
            self.predict_table.setItem(c,0,QTableWidgetItem(str(index)))
            self.predict_table.setItem(c,1,QTableWidgetItem(title))
            self.dict_[index] = QCheckBox()
            if self.checked[index]==1:
                self.dict_[index].setChecked(True)
            self.predict_table.setCellWidget(c,2,self.dict_[index])
            self.ch_dict_[index] = QCheckBox()
            if self.is_change[index]==1:
                self.ch_dict_[index].setChecked(True)
            self.predict_table.setCellWidget(c,3,self.ch_dict_[index])
            self.predict_table.setItem(c,4,QTableWidgetItem(str(pre)))
            c+=1

        self.label.setText('%s건 조회'%c)
    def save_file(self):
        print('clicked')
        for index, value in self.dict_.items():
            if value.isChecked():
                self.checked[index]=1
        for index, value in self.ch_dict_.items():
            if value.isChecked():
                self.is_change[index]=1
        content_list = []
        title_list = []
        noun_list = []
        label_list = []
        for ch,content,title,noun,label in zip(self.before_checked,self.data.loc[:,'content'],self.data.loc[:,'title'],self.data.loc[:,'nouns'],self.data.loc[:,'label']):
            content_list.append(content)
            title_list.append(title)
            noun_list.append(noun)
            if ch != 1:
                label_list.append(label)
            else:
                if label ==1:
                    label_list.append(0)
                else:
                    label_list.append(1)
        for checked, changed, title, content,noun,pre in zip(self.checked, self.is_change ,self.data_merged['title'],self.data_merged['content'],self.data_merged['nouns'],self.pre_list):
            if checked == 1:
                if pre >0.5:
                    if changed == 1:
                        pre=0
                    else:
                        pre=1
                else:
                    if changed == 1:
                        pre=1
                    else:
                        pre=0
                content_list.append(content)
                title_list.append(title)
                noun_list.append(noun)
                label_list.append(pre)

        new_file = pd.DataFrame({'content':content_list,'title':title_list,'nouns':noun_list,'label':label_list})
        if os.path.isdir('new_labelling_file')==False:
            os.mkdir('new_labelling_file')
        os.chdir('new_labelling_file')
        text, ok = QInputDialog.getText(self, '저장파일이름', '저장할 파일 이름:')
        file_c = 1
        while True:
            if os.path.isfile('new_labelling_file_%s_%s.xlsx'%(text,file_c)) == False:
                break
            else:
                file_c+=1
        
        self.new_full_name = 'new_labelling_file/new_labelling_file_%s_%s.xlsx'%(text,file_c)
        self.new_file_name = 'new_labelling_file_%s_%s.xlsx'%(text,file_c)
        new_file.to_excel(self.new_file_name)
        os.chdir('../')            
        print('저장완료')
        pass
    def retrain(self):
        self.save_file()
        self.hide()
        self.second = SecondWindow(fname = self.new_full_name)
        self.second.exec()
    def model_save(self):
        if os.path.isdir('saved_model')==False:
            os.mkdir('saved_model')
        os.chdir('saved_model')
        text, ok = QInputDialog.getText(self, '저장파일이름', '저장할 파일 이름(h5):')
        file_c = 1
        while True:
            if os.path.isfile('%s_%s.h5'%(text,file_c)) == False:
                break
            else:
                file_c+=1
        
        self.save_full_modelname = 'saved_model/%s_%s.xlsx'%(text,file_c)
        self.save_modelname = '%s_%s.h5'%(text,file_c)
        self.model.save(self.save_modelname)
        os.chdir('../')            
        print('저장완료')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )
