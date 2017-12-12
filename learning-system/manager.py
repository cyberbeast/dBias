import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,create_json_data,preprocess_data,get_validate_data,supervisor
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model,compute_metrics
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import pickle
import os

try:
    client = MongoClient('ds135926.mlab.com',35926)
    db = client['dbias']
    db.authenticate('admin','admin')
    collection = db.tasks
    report_collection = db.reports
except Exception as e:
    print ("Error: ",e)


path_files = {
    'Adult Census Income Dataset': 'data/adult.data'
}
#data = None
data = read_data('data/adult.data')
limit = 0
toggle_supervisor = True
def train(model_id):
    print("readched")
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
        if toggle_supervisor == False:
            print('Do user preprocess and mode calculation here')
            x,y = preprocess_data(data)
            yield('Preprocessed non-supervised data')
            model_rf = train_model(model_first,x[:limit],y[:limit])
            model_dt = train_model(model_second,x[:limit],y[:limit])
            yield("Trained non-supervised models")
            pickle.dump(model_rf, open('models/'+str(model_id)+model_first+'usr'+'.pkl', 'wb'))
            pickle.dump(model_dt, open('models/'+str(model_id)+model_second+'usr'+'.pkl', 'wb'))
            yield("Stored non-supervised models")
        x,y = supervisor(data)
        yield('Preprocessed supervised data')
        model_rf = train_model(model_first,x[:limit],y[:limit])
        model_dt = train_model(model_second,x[:limit],y[:limit])
        model_details['trained'] = True
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield('Trained supervised models')
        pickle.dump(model_rf, open('models/'+str(model_id)+model_first+'.pkl', 'wb'))
        pickle.dump(model_dt, open('models/'+str(model_id)+model_second+'.pkl', 'wb'))
        yield('Stored supervised models')
    else:
        yield ("Model already trained")
    report_gen = report_data(model_id)
    while True:
        try:
            yield(next(report_gen))
        except StopIteration:
            break
    model_details['action'] = False
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    yield ("Done")

def report_data(model_id):
    print("reached here")
    data = read_data('data/adult.data')
    pp = pprint.PrettyPrinter(indent=2)
    models = ['random_forest','decision_tree']
    attributes = list(data.columns.values)
    #report_document = report_collection.find_one({"task": ObjectId(model_id)})
    report_json = {}
    ## Make Toggle json
    if toggle_supervisor == False:
        ## Do User stuff here
        print("Processing user_report")
        usr_report = {}

    # Doing supervisor stuff
    sv_report = {}
    sv_report['visualization'] = []
    sv_report['visualization'].append(create_json_data(data)) #Push to viz data
    # Push data into json
    #report_collection.update({'task': ObjectId(model_id)}, {'$push':{'visualizations':create_json_data(data)}}, upsert=False)
    #yield("Data pushed to mongo")
    #path_heatmap = plot_heatmap(data) # Plot heatmap
    #path_scatterplot = plot_scatterplot(data)
    x,y = preprocess_data(data)
    report_json['models']=[]
    #yield("First Visualization done")
    for model_name in models:
        model_obj = {}
        if os.path.exists('models/'+str(model_id)+model_name+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'.pkl', 'rb'))
        else:
            continue
            #yield ("Model not found")
        pred = predict_model(model,x[24000:])
        data[model_name] = Series(predict_model(model,x)) # Add to data frame
        
        accuracy,classification_error,precision,recall,tn,fp,fn,tp = compute_metrics(data,model_name) # Send data to report
        model_obj = {
            'accuracy': accuracy*100,
            'classification_error': classification_error*100,
            "precision": precision*100,
            'recall': recall*100,
            'confusion_matrix': [int(tn), int(fp), int(fn), int(tp)],
            'feature_importance': model.feature_importances_.tolist()
        }
        if model_name == 'random_forest':
            model_obj['type']= 'rf'
        else:
            model_obj['type']= 'dt'
        #report_collection.update({'task': ObjectId(model_id)}, {'$push':{'models':model_obj}}, upsert=False)
    #yield("Model loaded and finished Calculating features")
    print("calculated model features")
    print(model_obj)

    # Calculate skewed data
    feature = 'race'
    skewed_values, unique_values = skew_calculator(data,feature) # Send Data to report
    multi = []
    for skew,feature in zip(skewed_values,unique_values):
        series=[]
        for sk,attri in zip(skew,attributes):
            series.append({
                'name':attri,
                'value':sk
            })
        data_point = {
            'name':feature,
            'series':series
        }
        multi.append(data_point)
        skewed_data={
        'name':'skewed data graph',
        'chartType': 'line',
        'feature': 'race',
        'multi':multi
    }
    print (skewed_data) # Push to viz data
    #yield("Model loaded second set of visualizations")
    #report_collection.update({'task': ObjectId(model_id)}, {'$push':{'visualizations':skewed_data}}, upsert=False)
    #yield("Report Generated")
    return 0



def main():
    print("running model")
    model_id = '5a2ddcfa878cd42cbf0269e3'
    print(report_data(model_id))
    print("done")
main()