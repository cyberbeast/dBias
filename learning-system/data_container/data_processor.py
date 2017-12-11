import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import sklearn.preprocessing as preprocessing
import pandas as pd
import numpy as np
import os

def filter_data(dataset,option='race',value='all'):
    if value !='all':
        mask= dataset[option] == value
        subset = dataset[mask]
    else:
        subset = dataset
    subset.fillna(0)
    features = dataset.columns
    values = []
    for i in features:
        try:
            values.append(stats.skew(subset[i]))
        except TypeError:
            label_encoding = preprocessing.LabelEncoder()
            subset[i] = label_encoding.fit_transform(subset[i])
            values.append(stats.skew(subset[i]))
    return values


def skew_calculator(data,feature):
    encoded_dataset = data.values
    features = data.columns
    variables = data[feature].unique()
    all_skew_values = []
    for variable in variables:
        list_skew_values = filter_data(data,feature,variable)
        all_skew_values.append(list_skew_values)
    all_skew_values.append(filter_data(data))
    return all_skew_values,variables # Return this for ng-chart
    # exit()
    # val1 = pd.DataFrame({'features':features,'values':val1})
    # val2 = pd.DataFrame({'features':features,'values':val2})
    # val3 = pd.DataFrame({'features':features,'values':val3})
    # fig, ax = plt.subplots()
    # sns.pointplot(x='features', y='values', data=val1, ax=ax, color='b')
    # sns.pointplot(x='features', y='values', data=val2, ax=ax, color='g')
    # sns.pointplot(x='features', y='values', data=val3, ax=ax, color='k')
    # ax.set_xticklabels(features, rotation=-30)
    # plt.savefig('skew.png')

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



def plot_heatmap(data):
    encoded_data, _ = number_encode_features(data)
    sns.heatmap(encoded_data.corr(), square=True)
    print("Encoded data",encoded_data.corr())
    plt.xticks(rotation='vertical')
    plt.yticks(rotation='horizontal')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.savefig('heatmap.png')
    return os.path.abspath('heatmap.png')

def plot_countData(data):
    print (data)
    
    return 0

def plot_scatterplot(data):
    sns.set(style="ticks")
    sns.pairplot(data, hue="class")
    plt.savefig('scatterplot.png')
    return os.path.abspath('scatterplot.png')