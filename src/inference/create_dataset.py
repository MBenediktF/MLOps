# Read the data from influx and s3 in order to create a new dataset
# with features and labels fron an measuerment

from log_message import log_message
import cv2
from uuid import uuid4
import os
from datetime import datetime
from influx_helpers import fetch_records
from s3_helpers import upload_image_from_buffer, upload_txt_from_dict
from s3_helpers import fetch_image


def create_dataset_from_measurement(measurement):
    # fetch datapoints from influx
    columns = ["feature_file_url", "sensor_value"]
    measurement = fetch_records(measurement, columns)

    # create dataset uid
    dataset_uuid = str(uuid4())

    # read images from s3
    for record in measurement:
        image_file_url = record["feature_file_url"]
        sensor_value = record["sensor_value"]
        image = fetch_image(image_file_url)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # scale image and convert to jpg
        is_success, image_buffer = cv2.imencode('.jpg', image)
        if not is_success:
            log_message("Could not encode image to JPEG format")
            continue

        # create image metadata string
        image_uuid = os.path.basename(image_file_url).split(".")[0]
        filename = f'datasets/{dataset_uuid}/{image_uuid}_{sensor_value}.jpg'

        # upload images as jpg to s3
        try:
            upload_image_from_buffer(image_buffer, filename)
        except Exception as e:
            log_message(f"Could not upload image to s3: {e}")
            continue

    # add metadata txt file to bucket
    metadata = {
        "dataset_uuid": dataset_uuid,
        "measurement": measurement,
        "num_images": len(measurement),
        "created_at": datetime.now().isoformat()
    }
    upload_txt_from_dict(metadata, f'datasets/{dataset_uuid}/metadata.txt')

    return dataset_uuid, len(measurement)
