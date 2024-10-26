from uuid import uuid4
from influx_helpers import write_record, create_record
from s3_helpers import upload_image_from_bytefile
from log_message import log_message, ERROR
from collect_image_characteristics import collect_image_characteristics


def log_features_prediction(
        feature_file,
        prediction,
        sensor_value,
        measurement="",
        model_name="",
        model_version=""
        ):
    try:
        # 1: Save image to S3
        feature_file_name = save_image_to_s3(feature_file, measurement)
        if not feature_file_name:
            raise ValueError("Invalid file type: Only .jpg files are allowed")
        # 2: Collect image characteristics
        image_characteristics = collect_image_characteristics(feature_file)
        # 3: Write data to InfluxDB
        write_inference_data_to_influx(
            feature_file_name,
            prediction,
            sensor_value,
            measurement,
            model_name,
            model_version,
            image_characteristics
            )
    except Exception as e:
        log_message(f"Error logging features prediction: {str(e)}", ERROR)


def write_inference_data_to_influx(
        image_url,
        prediction,
        sensor_value,
        measurement,
        model_name,
        model_version,
        image_characteristics
        ):
    if not isinstance(image_url, str):
        log_message("image_url has to be a str", ERROR)
        raise ValueError(f"image_url has to be a str, got {type(image_url)}")
    record = create_record(measurement) \
        .field("feature_file_url", image_url) \
        .field("prediction", prediction) \
        .field("sensor_value", sensor_value) \
        .field("model_name", model_name) \
        .field("model_version", model_version) \
        .field("image_characteristics", image_characteristics)
    write_record(record)


def save_image_to_s3(image_file, measurement):
    filename = f'features/{measurement}/{uuid4()}.jpg'
    try:
        upload_image_from_bytefile(image_file, filename)
    except Exception as e:
        log_message(f"Could not upload image to S3: {e}", ERROR)
        return False
    return filename
