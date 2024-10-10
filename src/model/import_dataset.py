from inference.s3_helpers import download_dataset, enable_local_dev
import numpy as np
from io import BytesIO
from PIL import Image

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 75

S3_ENDPOINT = "http://localhost:9000"
enable_local_dev(S3_ENDPOINT)

dataset_uuid = "ea93eb20-616c-4ad2-9d82-cca701766612"

dataset = download_dataset(dataset_uuid)
if not dataset:
    raise Exception("Could not download dataset")


images = np.zeros((len(dataset), IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
labels = np.zeros((len(dataset), 1), dtype=np.uint8)

for i, (filename, image) in enumerate(dataset.items()):
    try:
        images[i] = np.array(Image.open(BytesIO(image)))
    except Exception as e:
        print(f"Could not read image: {e}")
        continue
    labels[i] = int(filename.split('_')[-1].split('.')[0])

print(labels)
