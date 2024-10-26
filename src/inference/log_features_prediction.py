from uuid import uuid4
from influx_helpers import write_record, create_record
from s3_helpers import upload_image_from_bytefile
from log_message import log_message, ERROR


def log_features_prediction(
        feature_file,
        prediction,
        sensor_value,
        measurement="",
        model_name="",
        model_version=""
        ):
    feature_file_name = save_image_to_s3(feature_file, measurement)
    if not feature_file_name:
        log_message("Could not save image to S3", ERROR)
        raise ValueError("Invalid file type: Only .jpg files are allowed")
    write_inference_data_to_influx(
        feature_file_name,
        prediction,
        sensor_value,
        measurement,
        model_name,
        model_version
        )
    return


def write_inference_data_to_influx(
        image_url,
        prediction,
        sensor_value,
        measurement,
        model_name,
        model_version
        ):
    if not isinstance(image_url, str):
        log_message("image_url has to be a str", ERROR)
        raise ValueError(f"image_url has to be a str, got {type(image_url)}")
    record = create_record(measurement) \
        .field("feature_file_url", image_url) \
        .field("prediction", prediction) \
        .field("sensor_value", sensor_value) \
        .field("model_name", model_name) \
        .field("model_version", model_version)
    write_record(record)


def save_image_to_s3(image_file, measurement):
    filename = f'features/{measurement}/{uuid4()}.jpg'
    try:
        upload_image_from_bytefile(image_file, filename)
    except Exception as e:
        log_message(f"Could not upload image to S3: {e}", ERROR)
        return False
    return filename
