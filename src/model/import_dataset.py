from helpers.s3 import download_dataset
import numpy as np
from io import BytesIO
from PIL import Image


def import_dataset(dataset_uuid):
    dataset = download_dataset(dataset_uuid)
    if not dataset:
        raise Exception("Could not download dataset")

    # get image width and height
    first_image = next(iter(dataset.values()))
    img_width, img_height = Image.open(BytesIO(first_image)).size

    # restructure dataset
    images = np.zeros((len(dataset), img_height, img_width, 3), dtype=np.uint8)
    labels = np.zeros((len(dataset)), dtype=np.uint8)
    uids = np.zeros((len(dataset)), dtype='U36')
    for i, (filename, image) in enumerate(dataset.items()):
        try:
            images[i] = np.array(Image.open(BytesIO(image)))
        except Exception as e:
            print(f"Could not read image: {e}")
            continue
        labels[i] = int(filename.split('_')[-1].split('.')[0])
        uids[i] = filename.split('/')[2].split('_')[0]

    return images, labels, uids
