import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,dump_json,preprocess_data,get_validate_data
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
    print(model_details)
    if model_details['trained'] == False:
        if model_details['dataset'] =='Adult Census Income Dataset':
            path = path_files[model_details['dataset']]
            data = read_data(path)
            limit = int(0.8*data.shape[0])
            yield('finished loading data')
        else:
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
    model_details['action'] = True
    yield ("Done")

def report_file(model_id):
    pp = pprint.PrettyPrinter(indent=2)
    models = ['random_forest','decision_tree']
    attributes = data.columns
    # model_first = 'random_forest'
    # model_second = 'decision_tree'
    report = {}
    data_more_50,data_less_50 = dump_json(data)
    #plot_heatmap(data) # Plot heatmap
    #plot_scatterplot(data)
    more_50 = json.dumps(data_more_50) # send data to ng-chart
    less_50 = json.dumps(data_less_50) # send data to ng-chart
    report['data_more_50'] = more_50
    report['data_less_50'] = less_50

    x,y = preprocess_data(data)


    # # model
    # print ("Result from trained model")
    # print (np.bincount(data[model_first] == '>50K'))

    # # GT
    # print ("Ground Truth")
    # print (np.bincount(data['class'] == '>50K'))
    # bin_count = np.bincount(data['class'] == data[model_first])
    # print (bin_count)

    # Calculate metrices
    for model_name in models:
        if os.path.exists('models/'+str(model_id)+model_name+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'.pkl', 'rb'))
        else:
            continue
            #yield ("Model not found")
        pred = predict_model(model,x[24000:])
        data[model_name] = Series(predict_model(model,x)) # Add to data frame
        accuracy,classification_error,precision,recall = compute_metrics(data,model_name) # Send data to report
        report[model_name] = {}
        report[model_name]['accuracy'] = accuracy
        report[model_name]['classification_error'] = classification_error
        report[model_name]['precision'] = precision
        report[model_name]['recall'] = recall
    #model_details['accuracy'] = accuracy
    #collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)

    feature = 'race'
    skewed_data, unique_values = skew_calculator(data,feature) # Send Data to report
    skewed_values = [{"data": d, "label": l} for d,l in zip(skewed_data, unique_values)]
    report['skewed']=skewed_values
    report['attributes'] = attributes
    return report

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
    value = report_file(model_id)
    print(value['skewed'])
    print(value['attributes'])

