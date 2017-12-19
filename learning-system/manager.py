import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,create_json_data,preprocess_data,get_validate_data,supervisor_fn
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model,compute_metrics
from sklearn.metrics import accuracy_score
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import pickle
import os
from test_suite.classes import Query,Suite

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

def report_generate():
    
    return 0

def train(model_id):
    models = ['Random Forest','Decision Tree']
    not_parseable = ['fnlwgt','capital-gain','capital-loss','class']
    yield('Loading Task')
    model_details = collection.find_one({"_id": ObjectId(model_id)})
    model_details['action'] = True
    yield('Locking action')
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield('Updating action')
    skewed_data=['race']
    yield("Action: " + str(model_details['action']))
    if model_details['trained'] == False:
        yield('Model not trained')
        yield('Training now...')
        yield('Loading Dataset')
        if model_details['dataset'] =='Adult Census Income Dataset':
            yield('Loaded Dataset')
            path = path_files[model_details['dataset']]
            data = read_data(path)
            yield('Reading dataset')
            test_data = read_data('data/adult.data')
            attributes = list(data.columns.values)
            yield('Finished reading data')
        else:
            model_details['action'] = False
            collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
            yield ("Dataset not found")
        best_accuracy = {}
        yield('Checking supervisor')
        if model_details['supervisor'] == False:
            yield('Supervisor: OFF')
            '''
            Things to do here:
            1) Training accuracy and best model
            2) Make supervisor code
            '''
            # print('Do user preprocess and model calculation here')
            full_data = data
            x,y = preprocess_data(data)
            yield('Processing data')
            for i in models:
                trained_model = train_model(i,x,y)
                yield('Training Model: ' + i)
                pred = predict_model(trained_model,x)
                yield('Computing Training accuracy')
                accuracy = accuracy_score(y, pred)
                best_accuracy[i] = round(accuracy*100,2)
                yield("Trained Model: " + i)
                if not os.path.exists('models/'):
                    os.makedirs('dataset/')
                    yield('Serializing Model')
                    pickle.dump(trained_model, open('models/'+str(model_id)+i+'usr'+'.pkl', 'wb'))
                else:
                    pickle.dump(trained_model, open('models/'+str(model_id)+i+'usr'+'.pkl', 'wb'))
                yield("Serializing Complete...")
        index = supervisor_fn(data) # Change this later
        yield('SV: Analyzing...')
        data = data.loc[index]
        x,y = preprocess_data(data)
        x_test,y_test = preprocess_data(test_data)
        for i in models:
            yield('SV: Training Model: ' + i)
            trained_model = train_model(i,x,y)
            pred = predict_model(trained_model,x)
            yield('SV: Computing Training accuracy')            
            accuracy = accuracy_score(y, pred)
            best_accuracy[i] = round(accuracy*100,2)
            yield("SV: Trained Model " + i)            
            pickle.dump(trained_model, open('models/'+str(model_id)+i+'sv'+'.pkl', 'wb'))
            yield('SV: Serializing Model')
        maximum = max(best_accuracy, key=best_accuracy.get)
        yield('Deciding best model...')
        model_details['best_training_model'] = maximum
        model_details['best_training_accuracy'] = best_accuracy[maximum]
        model_details['trained']= True
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield('SV: Training Complete.')     
    else:
        yield ("Model already trained")
        model_details['action'] = False
        collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
        yield("Action: " + str(model_details['action']))
    report_document = report_collection.find_one({"task": ObjectId(model_id)})
    report_json = {}
    yield('Generating report')
    if model_details['supervisor'] == False:
        '''
        Things to do here
        1) make json for user report
        2) Add visualzations and model data
        3) push to report
        '''
        print("Processing user_report")
        ## Calculate visualization and model_data and store it in content
        content = []
        content_data = []
        for i in attributes:
            if i not in not_parseable:
                content.append({'type':'visualizations','data':create_json_data(full_data,i)})
        yield("Persisting Data")
        report_json['models']=[]
        yield("Distributed Salary Graph")
        for model_name in models:
            model_obj = {}
            if os.path.exists('models/'+str(model_id)+model_name+'usr'+'.pkl'):
                model = pickle.load(open('models/'+str(model_id)+model_name+'usr'+'.pkl', 'rb'))
            else:
                continue
                yield ("Model not found")
            pred = predict_model(model,x_test)
            data['usr_'+model_name] = Series(predict_model(model,x)) # Add to data frame
            data['usr_'+model_name].replace([None], ['>50K'], inplace=True)
            accuracy,classification_error,precision,recall,tn,fp,fn,tp = compute_metrics(test_data,model_name,pred) # Send data to report
            yield('Computing Model Metrics')
            model_obj = {
                'accuracy': round(accuracy,2)*100,
                'classification_error': round(classification_error*100,2),
                "precision": round(precision*100,2),
                'recall': round(recall*100,2),
                'confusion_matrix': [int(tn), int(fp), int(fn), int(tp)],
                'feature_importance': model.feature_importances_.tolist() # Make this into a graph
            }
            model_obj['type']= model_name
            content_data = {'type':'model_details','data':model_obj}
            content.append(content_data)
        yield("Skewed Data Graph")
        for feature in skewed_data:
            yield('Skewed Graph: ' + feature)
            if feature not in not_parseable:
                if skew_calculator(full_data,feature,attributes):
                    content.append({'type':'visualizations','data':skew_calculator(full_data,feature,attributes)})
            yield('Adding to user report')
            usr_report = {
            'type': 'u_report',
            'content': content
            }
        yield('Generating user report')
        report_collection.update({'task': ObjectId(model_id)}, {'$push':{'analysis':usr_report}}, upsert=False)
    # Doing supervisor stuff
    yield('SV: Generating report')
    content = []
    all_data = []
    content_data = []
    for i in attributes:
        yield('SV: Analyzing ' + i)
        if i not in not_parseable:
            content.append({'type':'visualizations','data':create_json_data(data,i)})
    yield("SV: Persisting data")
    report_json['models']=[]
    yield("SV: Distribution by Salary.")
    for model_name in models:
        model_obj = {}
        if os.path.exists('models/'+str(model_id)+model_name+'sv'+'.pkl'):
            model = pickle.load(open('models/'+str(model_id)+model_name+'sv'+'.pkl', 'rb'))
        else:
            continue
            yield ("Model not found")
        pred = predict_model(model,x_test)
        data[model_name] = Series(predict_model(model,x)) # Add to data frame
        data[model_name].replace([None], ['>50K'], inplace=True)
        accuracy,classification_error,precision,recall,tn,fp,fn,tp = compute_metrics(test_data,model_name,pred) # Send data to report
        yield('SV: Computing Model Metrics')
        
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
        elif model_name == 'Decision Tree' :
            model_obj['type']= 'Decision Tree'
        content_data = {'type':'model_details','data':model_obj}
        content.append(content_data)
    yield('SV: Model Metrics computed')
    # print("calculated model features")
    if not os.path.exists('dataset/'):
        os.makedirs('dataset/')
    pickle.dump(data, open('dataset/'+str(model_id)+'.pkl', 'wb'))
    
    # Calculate skewed data
    for feature in skewed_data:
        yield('SV: Analyzing ' + feature)
        if feature not in not_parseable:
            if skew_calculator(data,feature,attributes):
                content.append({'type':'visualizations','data':skew_calculator(data,feature,attributes)})
    yield("SV: Skewed Data graph.")
    yield("Adding to SV report.")
    sv_report = {
        'type':'sv_report',
        'content':content
        
    }
    report_collection.update({'task': ObjectId(model_id)}, {'$push':{'analysis':sv_report}}, upsert=False)
    yield("SV: Report Generated")
    model_details['action'] = False
    collection.update({'_id': ObjectId(model_id)}, {'$set': model_details}, upsert=False)
    yield("Action: " + str(model_details['action']))
    yield ("Done")



def test_suite(query,task_id):
    data = pickle.load(open('dataset/'+str(task_id)+'.pkl', 'rb'))
    print(type(query), query)
    query = json.loads(query)
    suite = Suite(data,"demo_suite")
    suite.add_query(query, "demo_query")
    out = next(suite.run())
    return out