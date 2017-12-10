import json
from data_container.data_loader import read_data,process_data,number_encode_features
from data_container.data_processor import plot_heatmap,skew_calculator
# Calculate the correlation and plot it
    
if __name__ == "__main__":
    path = 'data/adult.data'
    data = read_data(path)
    more_50,less_50 = process_data(data)
    encoded_data, _ = number_encode_features(data)
    plot_heatmap(encoded_data)
    skewed_data = skew_calculator(data)
    more_50 = json.dumps(more_50)
    less_50 = json.dumps(less_50)
