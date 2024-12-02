import boto3
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

s3_port = os.getenv('S3_PORT')
s3_endpoint = f"http://minio:{s3_port}"
s3_endpoint_local = f"http://localhost:{s3_port}"
s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')

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
