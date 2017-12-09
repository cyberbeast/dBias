import pandas as pd
from collections import Counter
import pprint
column_names = ['age','workclass','fnlwgt','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country','class']
def read_data(path):
    data = open(path)
    data = pd.read_csv(data,names=column_names,sep='\s*,\s*',encoding='ascii',engine='python')
    return data

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


    
if __name__ == "__main__":
    data = read_data('../adult.data')
    more_50,less_50 = process_data(data)
    pp = pprint.PrettyPrinter(indent=4)
    print pp.pprint(more_50)
