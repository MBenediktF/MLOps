# Read the data from influx and s3 in order to create a new dataset
# with features and labels fron an measuerment

import cv2
from uuid import uuid4
import os
from helpers.logs import log
from helpers.influx import fetch_records
from helpers.s3 import upload_image_from_bytefile
from helpers.s3 import fetch_image
from tables.datasets import store_dataset

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 75


def create_dataset_from_measurements(measurements):
    # create dataset uid
    dataset_uid = str(uuid4())
    num_records = 0

    for measurement_name in measurements:
        # fetch datapoints from influx
        columns = ["feature_file_url", "sensor_value"]
        measurement = fetch_records(measurement_name, columns)
        num_records += len(measurement)

        # read images from s3
        for record in measurement:
            image_file_url = record["feature_file_url"]
            sensor_value = record["sensor_value"]
            try:
                image = fetch_image(image_file_url)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            except Exception as e:
                log(f"Could not read {image_file_url} from s3: {e}")
                continue

            # skip measurements without a valid reference measurement
            if sensor_value == 0:
                continue

            # scale image and convert to jpg
            if image.shape[1] != IMAGE_WIDTH or image.shape[0] != IMAGE_HEIGHT:
                image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
            is_success, image_buffer = cv2.imencode('.jpg', image)
            if not is_success:
                log("Could not encode image to JPEG format")
                continue

            # create image metadata string
            image_uid = os.path.basename(image_file_url).split(".")[0]
            filename = f'datasets/{dataset_uid}/{image_uid}_{sensor_value}.jpg'

            # upload images as jpg to s3
            try:
                upload_image_from_bytefile(image_buffer.tobytes(), filename)
            except Exception as e:
                log(f"Could not upload image to s3: {e}")
                continue

    # store dataset metadata in mysql table
    store_dataset(dataset_uid, str(measurements), str(num_records))

    return dataset_uid, num_records
