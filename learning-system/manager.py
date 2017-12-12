import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,create_json_data,preprocess_data,get_validate_data,supervisor
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model,compute_metrics
from sklearn.metrics import accuracy_score
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
data = None

def train(model_id):
    models = ['Random Forest','Decision Tree']
    not_parseable = ['fnlwgt','capital-gain','capital-loss','class']
    model_details = collection.find_one({"_id": ObjectId(model_id)})
    model_details['action'] = True
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    if model_details['trained'] == False:
        if model_details['dataset'] =='Adult Census Income Dataset':
            path = path_files[model_details['dataset']]
            data = read_data(path)
            limit = int(0.8*24000)
            yield('finished loading data')
        else:
            model_details['action'] = False
            collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
            yield ("Dataset not found")
        if model_details['supervisor'] == False:
            '''
            Things to do here:
            1) Training accuracy and best model
            2) Make supervisor code
            '''
            print('Do user preprocess and model calculation here')
            x,y = preprocess_data(data)
            yield('Preprocessed non-supervised data')
            for i in models:
                trained_model = train_model(i,x[:limit],y[:limit])
                yield("Trained non-supervised models")
                pickle.dump(trained_model, open('models/'+str(model_id)+i+'usr'+'.pkl', 'wb'))
                yield("Stored non-supervised models")
        x,y = supervisor(data)
        yield('Preprocessed supervised data')
        best_accuracy = {}
        for i in models:
            trained_model = train_model(i,x[:limit],y[:limit])
            pred = predict_model(trained_model,x[:limit])
            accuracy = accuracy_score(y[:limit], pred)
            best_accuracy[i] = round(accuracy*100,2)
            yield("Trained supervised models")
            pickle.dump(trained_model, open('models/'+str(model_id)+i+'sv'+'.pkl', 'wb'))
            yield('Stored supervised models')
        maximum = max(best_accuracy, key=best_accuracy.get)
        model_details['best_training_model'] = maximum
        model_details['best_training_accuracy'] = best_accuracy[maximum]
        model_details['trained']= True
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield('Trained supervised models')     
    else:
        yield ("Model already trained")
        model_details['action'] = False
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield("Action: " + str(model_details['action']))
    print("Report generation starts here")
    attributes = list(data.columns.values)
    report_document = report_collection.find_one({"task": ObjectId(model_id)})
    report_json = {}
    if model_details['supervisor'] == False:
        '''
        Things to do here
        1) make json for user report
        2) Add visualzations and model data
        3) push to report
        '''
        print("Processing user_report")
        ## Calculate visualization and model_data and store it in content
        usr_report = {
            'type': 'user report',
            'content': []
        }

    # Doing supervisor stuff
    content = []
    #sv_report['visualization'] = []
    #sv_report['visualization'].append(create_json_data(data)) #Push to viz data
    # Push data into json
    all_data = []
    content_data = []
    for i in attributes:
        if i not in not_parseable:
            content.append({'type':'visualizations','data':create_json_data(data,i)})
    yield("Data pushed to mongo")
    #path_heatmap = plot_heatmap(data) # Plot heatmap
    #path_scatterplot = plot_scatterplot(data)
    x,y = preprocess_data(data)
    report_json['models']=[]
    yield("First Visualization done")
    for model_name in models:
        model_obj = {}
        if os.path.exists('models/'+str(model_id)+model_name+'sv'+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'sv'+'.pkl', 'rb'))
        else:
            continue
            yield ("Model not found")
        pred = predict_model(model,x[24000:])
        data[model_name] = Series(predict_model(model,x)) # Add to data frame
        accuracy,classification_error,precision,recall,tn,fp,fn,tp = compute_metrics(data,model_name) # Send data to report
        model_obj = {
            'accuracy': round(accuracy,2)*100,
            'classification_error': round(classification_error*100,2),
            "precision": round(precision*100,2),
            'recall': round(recall*100,2),
            'confusion_matrix': [int(tn), int(fp), int(fn), int(tp)],
            'feature_importance': model.feature_importances_.tolist() # Make this into a graph
        }
        if model_name == 'Random Forest':
            model_obj['type']= 'Random Forest'
        else:
            model_obj['type']= 'Decision Tree'
        content_data = {'type':'model_details','data':model_obj}
        content.append(content_data)
    print(content)
    yield("Model loaded and finished Calculating features")
    print("calculated model features")
    print(model_obj)

    # Calculate skewed data
    for feature in attributes:
        if feature not in not_parseable:
            if skew_calculator(data,feature,attributes):
                content.append({'type':'visualizations','data':skew_calculator(data,feature,attributes)})
    yield("Model loaded second set of visualizations")
    sv_report = {
        'type':'sv_report',
        'content':content
        
    }
    report_collection.update({'task': ObjectId(model_id)}, {'$push':{'analysis':sv_report}}, upsert=False)
    yield("Report Generated")
    model_details['action'] = False
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    yield ("Done")



def main():
    model_id = '5a2f45cce2a6d713f31cdee4'
    train(model_id)

main()