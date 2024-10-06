import csv
import os
import datetime
import boto3
from uuid import uuid4


S3_ENDPOINT = "http://minio:9000"
S3_ACCESS_KEY_ID = "minioadmin"
S3_SECRET_ACCESS_KEY = "minioadminpassword"
BUCKET_NAME = "mlops-research"

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)

log_file_csv = "logs/features_prediction.csv"


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


def save_image_to_s3(image_file, collection):
    if not file_is_jpg(image_file):
        return False
    filename = f'features/{collection}/{uuid4()}.jpg'
    s3_client.upload_fileobj(
        image_file,
        BUCKET_NAME,
        filename,
    )
    return True


def file_is_jpg(file):
    return file.filename.endswith(('.jpg', '.jpg'))
