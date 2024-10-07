import boto3
from uuid import uuid4
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


S3_ENDPOINT = "http://minio:9000"
S3_ACCESS_KEY_ID = "minioadmin"
S3_SECRET_ACCESS_KEY = "minioadminpassword"
BUCKET_NAME = "mlops-research"

INFLUX_ENDPOINT = "http://influxdb:8086"
INFLUX_ORG = "beg"
INFLUX_DATABASE = "inference_data_logs"
INFLUX_TOKEN = "influxadmintoken"


s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)

influx_api = InfluxDBClient(
    url=INFLUX_ENDPOINT,
    org=INFLUX_ORG,
    token=INFLUX_TOKEN,
).write_api(write_options=SYNCHRONOUS)


def log_features_prediction(endpoint, features, prediction):
    return


def save_to_influx(image_url, prediction, collection):
    record = Point("Measurement_Name") \
        .tag("collection", collection) \
        .field("image_url", image_url)
    influx_api.write(bucket=INFLUX_DATABASE,
                     org=INFLUX_ORG,
                     record=record)


def save_image_to_s3(image_file, collection):
    if not file_is_jpg(image_file):
        return False
    filename = f'features/{collection}/{uuid4()}.jpg'
    s3_client.upload_fileobj(
        image_file,
        BUCKET_NAME,
        filename,
    )
    save_to_influx(filename, "4", collection)
    return True


def file_is_jpg(file):
    return file.filename.endswith(('.jpg', '.jpg'))
