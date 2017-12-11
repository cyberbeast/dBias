import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,create_json_data,preprocess_data,get_validate_data
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot,plot_countData
from data_container.train_models import train_model,predict_model,compute_metrics
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import pickle
import os
from time import time
import pyimgur

CLIENT_ID = "42de006f84e71af"
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

data = None
limit = 0
toggle_supervisor = False
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
    report_gen = report(model_id)
    while True:
        try:
            yield(next(report_gen))
        except StopIteration:
            break
    model_details['action'] = False
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    yield ("Done")

def report(model_id):
    pp = pprint.PrettyPrinter(indent=2)
    models = ['random_forest','decision_tree']
    attributes = list(data.columns.values)
    report_document = report_collection.find_one({"task": ObjectId(model_id)})
    report_json = {}
    report_json['visualization'] = []
    report_json['visualization'].append(create_json_data(data))
    #report_collection.update({'task': ObjectId(model_id)}, {'$push':{'visualizations':create_json_data(data)}}, upsert=False)
    data_subset = create_json_data(data)
    print(data_subset)
    #yield("Data pushed to mongo")
    path_heatmap = plot_heatmap(data) # Plot heatmap
    path_scatterplot = plot_scatterplot(data)
    print (path_scatterplot)
    print(path_heatmap)
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path_heatmap, title="heatmap")
    print((uploaded_image.link))
    report_collection.update({'task':ObjectId(model_id) }, {'$push': {'visualizations':str(uploaded_image.link)}}, upsert=False)
    uploaded_image = im.upload_image(path_scatterplot, title="scatterplot")
    print(uploaded_image.link)
    report_collection.update({'task':ObjectId(model_id) }, {'$push': {'visualizations':str(uploaded_image.link)}}, upsert=False)
    x,y = preprocess_data(data)
    report_json['models']=[]
    yield("First Visualization done")
    for model_name in models:
        model_obj = {}
        if os.path.exists('models/'+str(model_id)+model_name+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'.pkl', 'rb'))
        else:
            continue
            yield ("Model not found")
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
        
        # model_obj['accuracy'] = 
        # model_obj['classification_error'] = classification_error*100
        # model_obj['precision'] = precision*100
        # model_obj['recall'] = recall*100
        # model_obj['confusion_matrix'] ={}
        # model_obj['confusion_matrix']['tn'] = tn
        # model_obj['confusion_matrix']['fp'] = fp
        # model_obj['confusion_matrix']['fn'] = fn
        # model_obj['confusion_matrix']['tp'] = tp
        # model_obj['feature_importance'] = model.feature_importances_
        # report_json['models'].append(model_obj)
        report_collection.update({'task': ObjectId(model_id)}, {'$push':{'models':model_obj}}, upsert=False)
    yield("Model loaded and finished Calculating features")
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
    yield("Model loaded second set of visualizations")
    #report_collection.update({'task': ObjectId(model_id)}, {'$push':{'visualizations':skewed_data}}, upsert=False)
    yield("Report Generated")

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

# if __name__ == '__main__':
    # model_id = '5a2ddcfa878cd42cbf0269e3'
    # print(report(model_id))
