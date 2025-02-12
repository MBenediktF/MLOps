# Read the data from influx and s3 in order to create a new dataset
# with features and labels fron an measuerment

import cv2
import os
from helpers.logs import Log, WARNING
from helpers.influx import fetch_records
from helpers.s3 import fetch_image
import numpy as np


def create_dataset(measurements, img_size, context=False):
    log = Log(context)

    img_width, img_height = img_size[2], img_size[1]

    images = []
    labels = []
    uids = []

    for measurement_name in measurements:
        # fetch datapoints from influx
        columns = ["feature_file_url", "sensor_value"]
        measurement = fetch_records(measurement_name, columns)

        # read images from s3
        for record in measurement:
            image_file_url = record["feature_file_url"]
            uid = os.path.basename(image_file_url).split(".")[0]
            label = record["sensor_value"]

            # skip measurements without a valid reference measurement
            if label == 0:
                continue

            # get image from s3 and add it to dataset
            try:
                image = fetch_image(image_file_url)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            except Exception as e:
                log.log(f"Could not read {image_file_url} from s3: {e}",
                        WARNING)
                continue

            # scale image and append
            if image.shape[1] != img_width or image.shape[0] != img_height:
                image = cv2.resize(image, (img_width, img_height))

            images.append(image)
            labels.append(label)
            uids.append(uid)

    # convert to np arrays
    images = np.array(images, dtype=np.uint8)
    labels = np.array(labels, dtype=np.uint16)
    uids = np.array(uids, dtype='U36')

    return images, labels, uids
