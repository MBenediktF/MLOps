from helpers.logs import Log, ERROR
from helpers.influx import write_record, create_record
from helpers.s3 import upload_image_from_bytefile
from uuid import uuid4

from collect_image_characteristics import collect_image_characteristics

# Keep measuremeent "Not selected" alive
write_record(create_record("Not selected").field("placeholder", 0))

log = Log()

def log_run(
        client_uid,
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
            client_uid,
            feature_file_name,
            prediction,
            sensor_value,
            measurement,
            model_name,
            model_version,
            image_characteristics
            )
    except Exception as e:
        log.log(f"Error logging features prediction: {str(e)}", ERROR)


def write_inference_data_to_influx(
        client_uid,
        image_url,
        prediction,
        sensor_value,
        measurement,
        model_name,
        model_version,
        image_characteristics
        ):
    if not isinstance(image_url, str):
        log.log("image_url has to be a str", ERROR)
        raise ValueError(f"image_url has to be a str, got {type(image_url)}")
    record = create_record(measurement) \
        .field("client_uid", client_uid) \
        .field("feature_file_url", image_url) \
        .field("prediction", prediction) \
        .field("sensor_value", sensor_value) \
        .field("model_name", model_name) \
        .field("model_version", model_version) \
        .field("brightness_mean", image_characteristics['brightness_mean']) \
        .field("brightness_std", image_characteristics['brightness_std']) \
        .field("red_mean", image_characteristics['red_mean']) \
        .field("green_mean", image_characteristics['green_mean']) \
        .field("blue_mean", image_characteristics['blue_mean']) \
        .field("red_std", image_characteristics['red_std']) \
        .field("green_std", image_characteristics['green_std']) \
        .field("blue_std", image_characteristics['blue_std']) \
        .field("lab_L", image_characteristics['lab_L']) \
        .field("lab_A", image_characteristics['lab_A']) \
        .field("lab_B", image_characteristics['lab_B']) \
        .field("hsv_H", image_characteristics['hsv_H']) \
        .field("hsv_S", image_characteristics['hsv_S']) \
        .field("hsv_V", image_characteristics['hsv_V']) \
        .field("edge_count", image_characteristics['edge_count']) \
        .field("contrast", image_characteristics['contrast']) \
        .field("dissimilarity", image_characteristics['dissimilarity']) \
        .field("homogeneity", image_characteristics['homogeneity']) \
        .field("ASM", image_characteristics['ASM']) \
        .field("energy", image_characteristics['energy']) \
        .field("correlation", image_characteristics['correlation']) \
        .field("keypoint_count", image_characteristics['keypoint_count'])
    write_record(record)


def save_image_to_s3(image_file, measurement):
    filename = f'features/{measurement}/{uuid4()}.jpg'
    try:
        upload_image_from_bytefile(image_file, filename)
    except Exception as e:
        log.log(f"Could not upload image to S3: {e}", ERROR)
        return False
    return filename
