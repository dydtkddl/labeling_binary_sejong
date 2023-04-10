import numpy as np
import pandas as pd
# from tensorflow import keras
from sklearn.model_selection import train_test_split 
import matplotlib.pyplot as plt
from konlpy.tag import Okt 
import pickle
import keras
from collections import Counter
from keras import layers
okt =Okt()
print('데이터 읽는중..')
with open('14000개데이터.pickle','rb' ) as f:
    data14000 = pd.DataFrame(pickle.load(f))

# from 프로젝트라벨링 import filename
# def n(x):
#     # print(np.array(x))
#     data = pd.read_excel(x).iloc[:, 1:4]
#     target = data.iloc[:,0]
#     data_lis = []
#     return data
class ClassificationModel():
    def __init__(self, labelfile ='',vocab_length = 500,label_column_name = '당첨자'):
        print('라벨링데이터 읽는중...')
        self.labeled_data =pd.read_excel(labelfile).loc[:,['title',label_column_name]]
        self.data = []
        self.vocab = []
        self.vocab_length = vocab_length
        self.target = self.labeled_data.loc[:,label_column_name]
        print('라벨링데이터로 최상위 %s개 단어사전 만드는 중..'%self.vocab_length)
        for title in self.labeled_data['title']:
            nouns = okt.nouns(title)
            self.vocab += nouns
            self.data.append(nouns)
        self.vocab =[x for x,y in sorted(Counter(self.vocab).items(), key=lambda x:-x[1])[:int(vocab_length)]]
        vocab = self.vocab
        print('idf만드는중')
        self.idf = np.zeros((self.vocab_length,))
        for tokenized in self.data:
            for key, value in Counter(tokenized).items():
                if key in self.vocab:
                    ind = self.vocab.index(key)
                    self.idf[ind]+=1
        self.idf = dict(pd.DataFrame({'idf':self.idf}).apply(lambda x: np.log(len(self.data)/(1+x))))['idf']
        print('tf만드는중..')
        self.tf = pd.DataFrame({'tokenized':self.data})['tokenized'].apply(lambda x: self.get_tf(x))
        print('tf_idf만드는중...')
        self.tf_idf = self.tf.apply(lambda x: x*self.idf)
    def get_tf(self,x):
        zeros = np.zeros((len(self.vocab),))
        for key, value in Counter(x).items():
            if key in self.vocab:
                ind = self.vocab.index(key)
                zeros[ind] = 1 + np.log(value)
        return zeros
    def for_predict_tfidf(self,v_data):
        vocab = self.vocab
        print('tf만드는중..')
        new_tf = v_data.apply(lambda x: self.get_tf(x))
        print('tf_idf만드는중...')
        new_tf_idf = new_tf.apply(lambda x: x*self.idf)
        return new_tf_idf
    def make_model(self, drop_rate=0):
        print('모델생성중..')
        self.model = keras.Sequential()
        model = self.model
        self.drop_rate = drop_rate
        self.dense01 = layers.Dense(units=(self.vocab_length)/2,activation = 'relu',input_shape = (self.vocab_length,))
        self.dense02 = layers.Dense(units=(self.vocab_length)/4,activation = 'relu')
        self.dense_out = layers.Dense(units = 1, activation='sigmoid')
        self.dropout = layers.Dropout(self.drop_rate)
        model.add(self.dropout);model.add(self.dense01);model.add(self.dropout)
        model.add(self.dense02);model.add(self.dropout);model.add(self.dense_out)    
        print('훈련 테스트 데이터 나누는중..')
        self.train_data, self.val_data, self.train_target, self.val_target = train_test_split(self.tf_idf, self.target, stratify=self.target, random_state=122, test_size=0.2)
    def compile(self):
        self.model.compile(optimizer = 'adam', loss='binary_crossentropy', metrics= 'accuracy')
    def train(self,epochs=10):
        self.epochs = epochs
        print('훈련시작')
        self.model.fit(self.train_data, self.train_target,epochs = self.epochs, validation_data=(self.val_data, self.val_target))
        print(1)
        return self.model
    def predict(self):
        model = self.model 
        all_data_14000 = data14000.loc[:,['title','nouns']]
        not_duplicated_data =pd.merge(all_data_14000, self.labeled_data.loc[:,['title']], how='outer',indicator=True)
        not_duplicated_data = not_duplicated_data[not_duplicated_data['_merge']=='left_only']
        pr_list = []
        for pre in model.predict(self.for_predict_tfidf(not_duplicated_data['nouns'])):
            if pre>0.5:
                pr_list.append(1)
            else:
                pr_list.append(0)
        
        return pr_list[:20]

    def inspect(self):
        model = self.model  
        self.one_one = []
        self.one_zero = []
        self.zero_one = []
        self.zero_zero = []
        self.predict_list = []
        for i in model.predict(self.val_data):
            if i >0.5:
                self.predict_list.append(1)
            else:
                self.predict_list.append(0)
        for real, pre,index  in zip(self.val_target,self.predict_list ,self.val_data.index ):
            if real == 1:
                if pre == real: 
                    #1, 1
                    self.one_one.append(index)
                else:
                    #1, 0 
                    self.one_zero.append(index)
            else:
                if pre == real: 
                    # 0, 0
                    self.zero_zero.append(index)
                else:
                    # 0, 1
                    self.zero_one.append(index)
    def show_inspect(self,real_label=1,pred=1):
        if real_label==1:
            if pred==1:
                return self.labeled_data.loc[self.one_one,'title']
            else:
                return self.labeled_data.loc[self.one_zero,'title']
        else:
            if pred == 1:
                return self.labeled_data.loc[self.zero_one,'title']
            else:
                return self.labeled_data.loc[self.zero_zero,'title']

# classifi = ClassificationModel(labelfile='합격자_str_라벨링작업물.xlsx')
# classifi.make_model()
# classifi.compile()
# classifi.train()
# classifi.model.summary()
# classifi.inspect()
# print(classifi.show_inspect())
# print('================================')
# print('================================')
# print(classifi.show_inspect(1,0))
# print('================================')
# print('================================')
# print(classifi.show_inspect(0,1))
# print('================================')
# print('================================')
# print(classifi.show_inspect(0,0))
# print('================================')
# print('================================')
# classifi.predict()