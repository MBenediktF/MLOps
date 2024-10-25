# Read the data from influx and s3 in order to create a new dataset
# with features and labels fron an measuerment

from log_message import log_message
import cv2
from uuid import uuid4
import os
from datetime import datetime
from inference.influx_helpers import fetch_records
from inference.s3_helpers import upload_image_from_bytefile
from inference.s3_helpers import upload_txt_from_dict
from inference.s3_helpers import fetch_image

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 75


def create_dataset_from_measurement(measurement_name):
    # fetch datapoints from influx
    columns = ["feature_file_url", "sensor_value"]
    measurement = fetch_records(measurement_name, columns)

    # create dataset uid
    dataset_uuid = str(uuid4())

    # read images from s3
    for record in measurement:
        image_file_url = record["feature_file_url"]
        sensor_value = record["sensor_value"]
        image = fetch_image(image_file_url)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # skip measurements without a valid reference measurement
        if sensor_value == 0:
            continue

        # scale image and convert to jpg
        if image.shape[1] != IMAGE_WIDTH or image.shape[0] != IMAGE_HEIGHT:
            image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        is_success, image_buffer = cv2.imencode('.jpg', image)
        if not is_success:
            log_message("Could not encode image to JPEG format")
            continue

        # create image metadata string
        image_uuid = os.path.basename(image_file_url).split(".")[0]
        filename = f'datasets/{dataset_uuid}/{image_uuid}_{sensor_value}.jpg'

        # upload images as jpg to s3
        try:
            upload_image_from_bytefile(image_buffer.tobytes(), filename)
        except Exception as e:
            log_message(f"Could not upload image to s3: {e}")
            continue

    # add metadata txt file to bucket
    metadata = {
        "dataset_uuid": dataset_uuid,
        "measurement": measurement_name,
        "num_images": len(measurement),
        "created_at": datetime.now().isoformat()
    }
    upload_txt_from_dict(metadata, f'datasets/{dataset_uuid}/metadata.txt')

    return dataset_uuid, len(measurement)
