import json
import numpy as np
from pandas import Series
from data_container.data_loader import read_data,dump_json,preprocess_data,get_validate_data
from data_container.data_processor import plot_heatmap,skew_calculator,plot_scatterplot
from data_container.train_models import train_model,predict_model
# Calculate the correlation and plot it
    
if __name__ == "__main__":
    path = 'data/adult.data'
    data = read_data(path)
    #more_50,less_50 = dump_json(data)
    plot_heatmap(data) # Plot heatmap, later convert to angular or send python image to client
    plot_scatterplot(data)
    #more_50 = json.dumps(more_50) send data to ng-chart
    #less_50 = json.dumps(less_50) send data to ng-chart

    ##### Training Phase #####
    x,y = preprocess_data(data)
    
    # Training models
    model_name = 'random_forest'
    model = train_model(model_name,x[:12000],y[:12000])

    # Predict models
    pred = predict_model(model,x[12000:13000])
    data[model_name] = Series(predict_model(model,x)) # Add to data frame

    # model
    print ("Result from trained model")
    print (np.bincount(data[model_name] == '>50K'))

    # GT
    print ("Ground Truth")
    print (np.bincount(data['class'] == '>50K'))

    ##### End Training #####

    #### Start Skewing #####
    feature = 'race'
    skewed_data,unique_values,headers = skew_calculator(data,feature) # Calculate skew
    # Pass the data to angular to visualize the graph

    #### End Skewing ######