import boto3
import numpy as np

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


def upload_file(file, filename):
    try:
        s3_client.upload_fileobj(
            file, BUCKET_NAME, filename)
    except Exception:
        return False
    return True


def upload_image_from_buffer(buffer, filename):
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=buffer.tobytes(),
        ContentType='image/jpeg'
    )


def upload_txt_from_dict(dict, file_path):
    dict_string = "\n".join(f"{key}: {value}" for key, value in dict.items())
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=file_path,
        Body=dict_string,
        ContentType='text/plain'
    )


def fetch_image(image_file_url):
    image = s3_client.get_object(Bucket=BUCKET_NAME, Key=image_file_url)
    image = image['Body'].read()
    image = np.frombuffer(image, np.uint8)
    if image.size == 0:
        raise Exception("Could not read image from s3")
    return image
