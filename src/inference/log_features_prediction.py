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
).write_api(
    write_options=SYNCHRONOUS)


def log_features_prediction(
        feature_file, prediction, sensor_value, collection="dev"):
    feature_file_name = save_image_to_s3(feature_file)
    if not feature_file_name:
        raise ValueError("Invalid file type: Only .jpg files are allowed")
    write_inference_data_to_influx(
        feature_file_name, prediction, sensor_value, collection)
    return


def write_inference_data_to_influx(
        image_url, prediction, sensor_value, collection):
    record = Point("Measurement_Name") \
        .tag("collection", collection) \
        .field("feature_file_url", image_url) \
        .field("prediction", prediction) \
        .field("sensor_value", sensor_value)
    influx_write_record(record)


def influx_write_record(record):
    influx_api.write(
        bucket=INFLUX_DATABASE,
        org=INFLUX_ORG,
        record=record)


def save_image_to_s3(image_file, collection):
    if not file_is_jpg(image_file):
        return False
    filename = f'features/{collection}/{uuid4()}.jpg'
    s3_client.upload_fileobj(
        image_file, BUCKET_NAME, filename,)
    return filename


def file_is_jpg(file):
    return file.filename.endswith(('.jpg', '.jpg'))
