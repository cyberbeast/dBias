import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier as RF

# def XGB_classifier(x,y):
#     model = XGBClassifier(max_depth=119, n_jobs=-1)
#     model.fit(x, y)
#     return model
#     return 0



def train_model(model_name,x,y):
    if model_name == 'random_forest':
        model_rf = RF(n_estimators=100, n_jobs=-1)
        model_rf.fit(x,y)
        return model_rf
    else:
        model_bad = RF(n_estimators=1)
        model_bad.fit(x,y)
        return model_bad


def predict_model(model,x):
    pred = model.predict(x)
    return pred


