import pandas as pd
from collections import Counter
import sklearn.preprocessing as preprocessing
import numpy as np
import os
from pandas import Series
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
    #for col in data.columns:
    #    try:
    #        data[col] = data[col].astype(int)
    #    except ValueError:
    #        pass
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



def main_deskew(data,class_no_prior,races_prior,no_over_yes,yes_over_no,X_train,Y):
    new_X = None
    _sum = 0
    print("No",no_over_yes)
    print("yes",yes_over_no)
    index = []
    for race in races_prior:
        print (race,)
        if races_prior[race]['no_prior'] >= class_no_prior:
            race_yes_index = data.index[(data['race'] == race) & (data['class']== True)].tolist()
            race_no_index = data.index[(data['race'] == race) & (data['class']== False)]
            race_no_index = np.random.choice(race_no_index,int(no_over_yes*len(race_yes_index)), replace=False).tolist()
        else:
            race_no_index = data.index[(data['race'] == race) & (data['class']== False)].tolist()
            race_yes_index = data.index[(data['race'] == race) & (data['class'] == True)]
            race_yes_index = np.random.choice(race_yes_index,int(yes_over_no*len(race_no_index)), replace=False).tolist()
        print (len(race_no_index)/ float(len(race_yes_index)+len(race_no_index)))
        _sum += len(race_no_index + race_yes_index)
        index = index+ race_no_index + race_yes_index
    print('no index',race_no_index)
    print('yes index',race_yes_index)
    print('index,',index)
    return index




def supervisor_fn(data_train):
    x = data_train.loc[:, data_train.columns != 'class']
    x = x.loc[:, x.columns != 'class']
    y = data_train['class']
    _class = data_train['class'] == '>50K'
    data_train['class'] = Series(_class)
    print('printvalues',data_train['class'])
    class_no_prior, class_yes_prior = get_distribution(data_train['class'])
    races_prior = {}
    for race in data_train['race'].unique():
        print('race',race)
        no, yes = get_distribution(data_train[data_train['race'] == race]['class'])
        races_prior[race] = {'no_prior':no, 'yes_prior':yes}
    all_no, all_yes = np.bincount(data_train['class'])
    yes_over_no = all_yes/float(all_no)
    no_over_yes = 1/yes_over_no
    print("classes_no_prior",class_no_prior)
    index = main_deskew(data_train,class_no_prior,races_prior,no_over_yes,yes_over_no,x,y)
    data_train['class'].replace([True, False], ['>50K', '<=50K'], inplace=True)
    return index
    
def get_validate_data(X_,Y):
    ratio = 0.9
    k=int(ratio*X_.shape[1])
    model_kbest = SelectKBest(k=k)

    X_new = model_kbest.fit_transform(X_, Y)

    mask = model_kbest.get_support(True)
    mask.shape
    return X_new


def get_distribution(distr_sample):
    type_a, type_b = np.bincount(distr_sample)
    total = float(len(distr_sample))
    return type_a/total, type_b/total

