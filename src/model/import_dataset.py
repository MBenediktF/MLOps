from inference.s3_helpers import download_dataset, enable_local_dev
import numpy as np
from io import BytesIO
from PIL import Image

# @TODO get this from the dataset
width = 100
height = 75

# @TODO get this from environment
S3_ENDPOINT = "http://localhost:9000"
enable_local_dev(S3_ENDPOINT)


def import_dataset(dataset_uuid):
    dataset = download_dataset(dataset_uuid)
    if not dataset:
        raise Exception("Could not download dataset")

    images = np.zeros((len(dataset), height, width, 3), dtype=np.uint8)
    labels = np.zeros((len(dataset), 1), dtype=np.uint8)

    for i, (filename, image) in enumerate(dataset.items()):
        try:
            images[i] = np.array(Image.open(BytesIO(image)))
        except Exception as e:
            print(f"Could not read image: {e}")
            continue
        labels[i] = int(filename.split('_')[-1].split('.')[0])

    return images, labels, width, height
