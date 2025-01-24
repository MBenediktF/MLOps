import boto3
import numpy as np
from dotenv import load_dotenv
import os
import json

load_dotenv()

host = os.getenv('HOST')
s3_port = os.getenv('S3_PORT')
s3_endpoint = f"http://minio:{s3_port}"
s3_endpoint_local = f"{host}:{s3_port}"
s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')
minio_ui_port = os.getenv('MINIO_UI_PORT')


s3_client = boto3.client(
    's3',
    endpoint_url=s3_endpoint,
    aws_access_key_id=s3_access_key_id,
    aws_secret_access_key=s3_secret_access_key
)


def enable_local_dev():
    global s3_client
    s3_client = boto3.client(
        's3',
        endpoint_url=s3_endpoint_local,
        aws_access_key_id=s3_access_key_id,
        aws_secret_access_key=s3_secret_access_key
    )


def upload_image_from_bytefile(bytefile, filename):
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=bytefile,
            ContentType='image/jpeg'
        )
    except Exception as e:
        raise e
    return True


def fetch_image(image_file_url):
    image = s3_client.get_object(Bucket=bucket_name, Key=image_file_url)
    image = image['Body'].read()
    image = np.frombuffer(image, np.uint8)
    if image.size == 0:
        raise Exception("Could not read image from s3")
    return image


def save_json_file(data, filename):
    try:
        json_data = json.dumps(data)
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json_data
        )
    except Exception as e:
        raise e
    return True


def load_json_file(filename):
    try:
        file = s3_client.get_object(Bucket=bucket_name, Key=filename)
        json_data = file['Body'].read().decode('utf-8')
        data = json.loads(json_data)
    except Exception as e:
        raise e
    return data


def save_model_file(filepath, filename):
    try:
        s3_client.upload_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=filename
        )
    except Exception as e:
        raise e
    return True


def load_model_file(filename, filepath):
    try:
        s3_client.download_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=filename
        )
    except Exception as e:
        raise e
    return True


def get_minio_filebrowser_url(filename):
    return f"{host}:{minio_ui_port}/browser/{bucket_name}/{filename}"
