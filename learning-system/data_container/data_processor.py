import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import sklearn.preprocessing as preprocessing
import pandas as pd
import numpy as np


def filter_data(dataset,option='race',value='all'):
    if value !='all':
        mask= dataset[option] == value
        subset = dataset[mask]
    else:
        subset = dataset
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


def skew_calculator(data):
    encoded_dataset = data.values
    features = list(data.columns.values)
    val1= filter_data(data,'race','White')
    val2 = filter_data(data,'race','Black')
    val3 = filter_data(data)
    val1 = pd.DataFrame({'features':features,'values':val1})
    val2 = pd.DataFrame({'features':features,'values':val2})
    val3 = pd.DataFrame({'features':features,'values':val3})
    fig, ax = plt.subplots()
    sns.pointplot(x='features', y='values', data=val1, ax=ax, color='b')
    sns.pointplot(x='features', y='values', data=val2, ax=ax, color='g')
    sns.pointplot(x='features', y='values', data=val3, ax=ax, color='k')
    ax.set_xticklabels(features, rotation=-30)
    plt.savefig('skew.png')
    return 0

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
    plt.xticks(rotation='vertical')
    plt.yticks(rotation='horizontal')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.savefig('heatmap.png')
    return 0

def plot_scatterplot(data):
    sns.set(style="ticks")
    sns.pairplot(data, hue="class")
    plt.savefig('scatterplot.png')