import pandas as pd
from collections import Counter
import sklearn.preprocessing as preprocessing
import numpy as np
import os
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest

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
def create_json_data(data,feature):
    data['class'] = data['class'].map(lambda x: x.strip())
    data_less50 = data.loc[data['class'] == '<=50K']
    data_more50 = data.loc[data['class'] == '>50K']
    categories = ['<=50K','>50K']
    store_values = {}
    obj = []
    for category in categories:
        count_values = None
        if category == '<=50K':
            count_values = Counter(data_less50[feature])       
        else:
            count_values = Counter(data_more50[feature])
        values = list(count_values.values())
        categories = {
            'data': values,
            'label': category
        }
        obj.append(categories)
    labels = list(count_values.keys())
    store_values={
        'name':'DistributionBySalary',
        'chartType':'bar',
        'feature':feature,
        'chartData': obj,
        'chartLabels':labels,
        'chartOptions':
        {
            'responsive': True
        },
        'chartLegend': True
    }
    return store_values

    '''
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
    counter_values_below_50={k: dict(v) for k, v in counter_values_below_50.items()}
    counter_values_above_50={k: dict(v) for k, v in counter_values_above_50.items()}'''
    #return counter_values_above_50,counter_values_below_50
    return 0

def preprocess_data(data):
    encoded_x = None
    numeric_x = None
    X = data.fillna(0).loc[:, data.columns != 'class'].values
    X[X == '?'] = '0'
    Y = data['class']
    for i in range(0, X.shape[1]):
        if type(X[0,i]) != str:
            if numeric_x is None:
                numeric_x = X[:,i].reshape(X.shape[0], 1)
            else:
                numeric_x = np.concatenate((X[:,i].reshape(X.shape[0], 1), numeric_x), axis=1)
            continue
        label_encoder = LabelEncoder()
        feature = label_encoder.fit_transform(X[:,i])
        feature = feature.reshape(X.shape[0], 1)
        onehot_encoder = OneHotEncoder(sparse=False)
        feature = onehot_encoder.fit_transform(feature)
        if encoded_x is None:
            encoded_x = feature
        else:
            encoded_x = np.concatenate((encoded_x, feature), axis=1)
    X_ = np.concatenate((numeric_x, encoded_x), axis=1)
    return X_,Y

def supervisor(data):
    encoded_x = None
    numeric_x = None
    X = data.fillna(0).loc[:, data.columns != 'class'].values
    X[X == '?'] = '0'
    Y = data['class']
    for i in range(0, X.shape[1]):
        if type(X[0,i]) != str:
            if numeric_x is None:
                numeric_x = X[:,i].reshape(X.shape[0], 1)
            else:
                numeric_x = np.concatenate((X[:,i].reshape(X.shape[0], 1), numeric_x), axis=1)
            continue
        label_encoder = LabelEncoder()
        feature = label_encoder.fit_transform(X[:,i])
        feature = feature.reshape(X.shape[0], 1)
        onehot_encoder = OneHotEncoder(sparse=False)
        feature = onehot_encoder.fit_transform(feature)
        if encoded_x is None:
            encoded_x = feature
        else:
            encoded_x = np.concatenate((encoded_x, feature), axis=1)
    X_ = np.concatenate((numeric_x, encoded_x), axis=1)
    return X_,Y

def get_validate_data(X_,Y):
    ratio = 0.9
    k=int(ratio*X_.shape[1])
    model_kbest = SelectKBest(k=k)

    X_new = model_kbest.fit_transform(X_, Y)

    mask = model_kbest.get_support(True)
    mask.shape
    return X_new