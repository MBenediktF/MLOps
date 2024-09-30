import csv
import os
import datetime


log_file_csv = "features_prediction_log.csv"


# Initialize csv if not already existing
if not os.path.exists(log_file_csv):
    with open(log_file_csv, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Endpoint', 'Feature', 'Prediction'])


def log_features_prediction(endpoint, features, prediction):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_csv, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, endpoint, features, prediction])
