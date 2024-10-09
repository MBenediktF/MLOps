from uuid import uuid4
from influx_helpers import write_record, create_record
from s3_helpers import upload_file


def log_features_prediction(
        feature_file, prediction, sensor_value, measurement="dev"):
    feature_file_name = save_image_to_s3(feature_file, measurement)
    if not feature_file_name:
        raise ValueError("Invalid file type: Only .jpg files are allowed")
    write_inference_data_to_influx(
        feature_file_name, prediction, sensor_value, measurement)
    return


def write_inference_data_to_influx(
        image_url, prediction, sensor_value, measurement):
    if not isinstance(image_url, str):
        raise ValueError(f"image_url has to be a str, got {type(image_url)}")
    record = create_record(measurement) \
        .field("feature_file_url", image_url) \
        .field("prediction", prediction) \
        .field("sensor_value", sensor_value)
    write_record(record)


def save_image_to_s3(image_file, measurement):
    if not file_is_jpg(image_file):
        return False
    filename = f'features/{measurement}/{uuid4()}.jpg'
    upload_file(image_file, filename)
    return filename


def file_is_jpg(file):
    return file.filename.endswith(('.jpg', '.jpg'))
