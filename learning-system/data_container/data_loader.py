import pandas as pd
from collections import Counter
import sklearn.preprocessing as preprocessing
import numpy as np
import os
import seaborn as sns

column_names = ['age','workclass','fnlwgt','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country','class']

cur_path = os.path.dirname(__file__)

'''
Read the data from csv
'''
def read_data(path):
    data = open(path)
    #column_names = list(data.columns.values)
    data = pd.read_csv(data,sep='\s*,\s*',encoding='ascii',names = column_names,engine='python')
    return data

'''
Make two dictionaries for count of featres<=50K & >50K
'''
def process_data(data):
    column_names = list(data.columns.values)
    counter_values_above_50 = {}
    counter_values_below_50 = {}
    # Error in class variables, unwanted white spaces removed in following line
    data['class'] = data['class'].map(lambda x: x.strip())
    data_less50 = data.loc[data['class'] == '<=50K']
    data_more50 = data.loc[data['class'] == '>50K']
    for i in column_names:
        if i =='fnlwgt':
            continue
        counter_values_below_50[i] = Counter(data_less50[i])
        counter_values_above_50[i] = Counter(data_more50[i])
    counter_values_below_50={k: dict(v) for k, v in counter_values_below_50.iteritems()}
    counter_values_above_50={k: dict(v) for k, v in counter_values_above_50.iteritems()}
    return counter_values_above_50,counter_values_below_50

'''
Encode features intp numbers making it easier to make cor-relation matrix
'''
def number_encode_features(data):
    result = data.copy()
    encoders = {}
    for column in result.columns:
        if result.dtypes[column] == np.object:
            encoders[column] = preprocessing.LabelEncoder()
            result[column] = encoders[column].fit_transform(result[column])
    return result, encoders