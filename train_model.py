import numpy as np
import pandas as pd
# from tensorflow import keras
from sklearn.model_selection import train_test_split 
from konlpy.tag import Okt
import pickle
from collections import Counter
import time
from collections import Counter
import re
from tensorflow import keras
from keras import layers
import openpyxl
okt =Okt()
def read_all_data():
    with open('14000개데이터.pickle','rb' ) as f:
        data14000 = pd.DataFrame(pickle.load(f))
    return data14000
def read_label_data(filename,label_name = '당첨자'):
    data= pd.read_excel(filename)
    data = data.loc[:,['title','content',label_name,'nouns']]
    return data
def mk_vocab(data,vocab_length):
    try:
        noun_list= []
        for nouns in data.loc[:,'nouns']:
            noun_list+=re.sub('[^ㄱ-힣]', ' ',nouns).split()
        vocab = sorted(Counter(noun_list).items(), key=lambda x:-x[1])[:int(vocab_length)]
        return vocab
    except:
        print('mk_vocab')

def mk_vt(data,tf_log, idf_log,vocab_length,vocab,all_data_length):
    # print(data)
    data = data['nouns']
    idf = np.zeros((int(vocab_length),))
    for i in data:
        i=re.sub('[^ㄱ-힣]', ' ',i).split()
        for key in i:
            if key in vocab:
                ind = vocab.index(key)
                idf[ind]+=1
    if idf_log==10:
        idf = np.log10(all_data_length/(idf+1))
    elif idf_log == 'e':
        idf = np.log(all_data_length/(idf+1))
    else:
        idf = np.log2(all_data_length/(idf+1))

    tf = data.apply(lambda x:a(x,vocab_length,vocab,tf_log))
    tf_idf = tf.apply(lambda x:x*idf )
    tf_idf = pd.DataFrame(dict(tf_idf).values())
    return tf_idf,idf
def a(record,vocab_length,vocab,tf_log):
    ze = np.zeros((vocab_length,))
    record=re.sub('[^ㄱ-힣]', ' ',record).split()
    for key, value in Counter(record).items():
        if key in vocab:
            ind = vocab.index(key)
            if tf_log == 'e':
                ze[ind]=1+np.log(value)
            elif tf_log=='10':
                ze[ind]=1+np.log10(value)
            else:
                ze[ind]=1+np.log2(value)
    return ze
                

def mk_model(dr01, dr02, dr03, ar01,ar02,ar03,vocab_length):
    model = keras.Sequential()
    model.add(layers.Dropout(dr01))
    model.add(layers.Dense(units=vocab_length/2,activation=ar01, input_shape = (vocab_length,)))
    model.add(layers.Dropout(dr02))
    model.add(layers.Dense(units =vocab_length/4,activation=ar02))
    model.add(layers.Dropout(dr03))
    model.add(layers.Dense(1,activation=ar03))
    print(ar01, ar02, ar03)
    model.compile(optimizer = 'adam',loss='binary_crossentropy',metrics = 'accuracy')
    return model
def split_data(tf_idf, target):
    try:
        train_data, test_data, train_target, test_target = train_test_split(tf_idf, target, test_size = 0.2, random_state=122,stratify=target)
    except:
        train_data, test_data, train_target, test_target = train_test_split(tf_idf, target, test_size = 0.2, random_state=122)
    return train_data, test_data, train_target, test_target
def train_model(model,tf_idf,target,epochs,train_data, test_data, train_target,test_target):
    print('trd',train_data.shape)
    print('ted',test_data.shape)
    print('trt',train_target.shape)
    print('tet',test_target.shape)
    history = model.fit(train_data, train_target,epochs = epochs,validation_data = (test_data, test_target))
    return model, history
def test_model(model,tf_idf):
    pre = model.predict(tf_idf)
    return pre 
def predict(model, data14000,data,tf_log, idf_log,vocab_length,vocab):
    data14000['nouns']=data14000['nouns'].astype('str')
    data['nouns']=data['nouns'].astype('str')
    data_merged = pd.merge(data14000, data, how = 'outer',indicator=True)
    data_merged = data_merged[data_merged['_merge']=='left_only'].drop_duplicates()
    data_merged.drop('_merge',axis= 1)
    new_data_nouns = data_merged['nouns']
    idf = np.zeros((int(vocab_length),))
    all_data_length = len(data14000)
    for i in new_data_nouns:
        i=re.sub('[^ㄱ-힣]', ' ',str(i)).split()
        for key in i:
            if key in vocab:
                ind = vocab.index(key)
                idf[ind]+=1
    if idf_log==10:
        idf = np.log10(all_data_length/(idf+1))
    elif idf_log == 'e':
        idf = np.log(all_data_length/(idf+1))
    else:
        idf = np.log2(all_data_length/(idf+1))

    tf = new_data_nouns.apply(lambda x:a(x,vocab_length,vocab,tf_log))
    tf_idf = tf.apply(lambda x:x*idf )
    tf_idf = pd.DataFrame(dict(tf_idf).values())
    pre_list = model.predict(tf_idf)
    return pre_list,data_merged
def evaluate(model, test_data, test_target):
    ev = model.evaluate(test_data,test_target)
    return ev