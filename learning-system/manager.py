import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,dump_json,preprocess_data,get_validate_data
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model,compute_metrices
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

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

def train(model_id):
    model_name = 'random_forest'
    report ={}
    model_details = collection.find_one({"_id": ObjectId(model_id)})
    if model_details['trained'] == False:
        if model_details['dataset'] =='Adult Census Income Dataset':
            path = path_files[model_details['dataset']]
            data = read_data(path)
            yield('finished loading data')
        else:
            yield ("Dataset not found")
        x,y = preprocess_data(data)
        model = train_model(model_name,x[:24000],y[:24000])
        model_details['trained'] = True
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield('Model Trained')
    else:
        yield ("Model already trained")
    yield ("Done")

def report():
    path = 'data/adult.data'
    model_name = 'random_forest'
    report ={}
    pp = pprint.PrettyPrinter(indent=2)
    if model_details['dataset'] =='Adult Census Income Dataset':
        data = read_data(path)
    else:
        print ("Dataset not found")
    data_more_50,data_less_50 = dump_json(data)

    plot_heatmap(data) # Plot heatmap
    plot_scatterplot(data)
    more_50 = json.dumps(data_more_50) # send data to ng-chart
    less_50 = json.dumps(data_less_50) # send data to ng-chart
    report['data_more_50'] = more_50
    report['data_less_50'] = less_50

    x,y = preprocess_data(data)

    pred = predict_model(model,x[24000:])
    data[model_name] = Series(predict_model(model,x)) # Add to data frame
    
    # model
    print ("Result from trained model")
    print (np.bincount(data[model_name] == '>50K'))

    # GT
    print ("Ground Truth")
    print (np.bincount(data['class'] == '>50K'))
    bin_count = np.bincount(data['class'] == data[model_name])
    print (bin_count)

    # Calculate metrices
    accuracy,classification_error,precision,recall = compute_metrices(data,model_name) # Send data to report
    report['metrics'] = {}
    report['metrics']['accuracy'] = accuracy
    report['metrics']['classification_error'] = classification_error
    report['metrics']['precision'] = precision
    report['metrics']['recall'] = recall
    model_details['accuracy'] = accuracy
    #collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)

    feature = 'race'
    skewed_data,unique_values,headers = skew_calculator(data,feature) # Send Data to report
    report['skewed']={}
    report['skewed']['data'] = skewed_data
    report['skewed']['features'] = unique_values
    report['skewed']['xlabels'] = headers
    return report