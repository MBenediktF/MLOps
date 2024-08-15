import boto3
import os


def get_file_content_from_s3(bucket_name, path):
    s3 = boto3.client('s3')

    try:
        # Datei aus S3 abrufen
        s3_object = s3.get_object(Bucket=bucket_name, Key=path)
        # Dateiinhalt als Text lesen
        file_content = s3_object['Body'].read().decode('utf-8')
        return file_content
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None


if __name__ == "__main__":
    # Name des Buckets aus der Umgebungsvariable abrufen
    bucket_name = os.environ.get('BUCKET_NAME')
    print(f"BUCKET_NAME is set to: {bucket_name}")

    if not bucket_name:
        print("Error: BUCKET_NAME environment variable not set.")
        exit(1)

    # S3-Schlüssel (Pfad zur Datei im S3-Bucket)
    path = 'datasets/ds2/ds2.txt'

    # Dateiinhalt abrufen
    content = get_file_content_from_s3(bucket_name, path)

    if content:
        print("File content:")
        print(content)
    else:
        print("Failed to retrieve the file content.")