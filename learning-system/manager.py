import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,create_json_data,preprocess_data,get_validate_data
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model,compute_metrics
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import pickle
import os
from time import time

try:
    client = MongoClient('ds135926.mlab.com',35926)
    db = client['dbias']
    db.authenticate('admin','admin')
    collection = db.tasks
except Exception as e:
    print ("Error: ",e)


path_files = {
    'Adult Census Income Dataset': 'data/adult.data'
}

data = None
limit = 0
def train(model_id):
    model_first = 'random_forest'
    model_second = 'decision_tree'
    global data
    global limit
    model_details = collection.find_one({"_id": ObjectId(model_id)})
    model_details['action'] = True
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    if model_details['trained'] == False:
        if model_details['dataset'] =='Adult Census Income Dataset':
            path = path_files[model_details['dataset']]
            data = read_data(path)
            limit = int(0.8*data.shape[0])
            yield('finished loading data')
        else:
            model_details['action'] = False
            yield ("Dataset not found")
            
        x,y = preprocess_data(data)
        model_rf = train_model(model_first,x[:limit],y[:limit])
        model_dt = train_model(model_second,x[:limit],y[:limit])
        model_details['trained'] = True
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield('Model Trained')
        pickle.dump(model_rf, open('models/'+str(model_id)+model_first+'.pkl', 'wb'))
        pickle.dump(model_dt, open('models/'+str(model_id)+model_second+'.pkl', 'wb'))
        yield('Model Dumped')
    else:
        yield ("Model already trained")
    model_details['action'] = False
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    yield ("Done")

def report(model_id):
    pp = pprint.PrettyPrinter(indent=2)
    models = ['random_forest','decision_tree']
    attributes = data.columns
    report_json = {}
    report_json['visualization'] = []
    report_json['visualization'].append(create_json_data(data))
    #plot_heatmap(data) # Plot heatmap
    #plot_scatterplot(data)
    x,y = preprocess_data(data)
    report_json['models']=[]
    for model_name in models:
        model_obj = {}
        if os.path.exists('models/'+str(model_id)+model_name+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'.pkl', 'rb'))
        else:
            continue
            #yield ("Model not found")
        pred = predict_model(model,x[24000:])
        data[model_name] = Series(predict_model(model,x)) # Add to data frame
        accuracy,classification_error,precision,recall,confusion_matrix = compute_metrics(data,model_name) # Send data to report
        if model_name == 'random_forest':
            model_obj['type']= 'rf'
        else:
            model_obj['type']= 'dt'
        model_obj['accuracy'] = accuracy*100
        model_obj['classification_error'] = classification_error*100
        model_obj['precision'] = precision*100
        model_obj['recall'] = recall*100
        model_obj['confusion_matrix'] = confusion_matrix
        model_obj['feature_importance'] = model.feature_importances_
        report_json['models'].append(model_obj)
    skewed_data={}
    skewed_data['name']='v2'
    skewed_data['chartType']='line'
    skewed_data['sets'] = []
    feature = 'race'
    skewed_values, unique_values = skew_calculator(data,feature) # Send Data to report
    new_obj = {}
    new_obj['feature']=feature
    #for d,l in zip(skewed_data,unique_values):
    types = [{"y": d, "x": attributes,"category":l} for d,l,a in zip(skewed_values, unique_values,attributes)]
    new_obj['types']=types
    skewed_data['sets'].append(new_obj)
    report_json['visualization'].append(skewed_data)
    return report_json

# def test_main():
#     path = 'data/adult.data'
#     print(path)
#     skewed_values = []
#     data = read_data(path)
#     feature = 'race'
#     headers = data.columns
#     skewed_data,unique_values = skew_calculator(data,feature)
#     iterative = False
#     s = time()
#     if iterative:
#         for d,l in zip(skewed_data, unique_values):
#             yield {"data": d, "label": l}
#     else:
#         skewed_values = [{"data": d, "label": l} for d,l in zip(skewed_data, unique_values)]
#     print(time()-s,"secs")

if __name__ == '__main__':
    model_id = '5a2ddcfa878cd42cbf0269e3'

