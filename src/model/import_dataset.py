from inference.s3_helpers import download_dataset, enable_local_dev
import numpy as np

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 75

S3_ENDPOINT = "http://localhost:9000"
enable_local_dev(S3_ENDPOINT)

dataset_uuid = "20b0b48e-ec06-48a1-aa54-3afc28b11585"

dataset = download_dataset(dataset_uuid)
if not dataset:
    raise Exception("Could not download dataset")

print(dataset)
print(len(dataset))

# images = np.zeros((len(dataset), IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
# labels = np.zeros((len(dataset), 1), dtype=np.uint8)

# for i, image in enumerate(dataset):
    # images[i] = image['image']
    # labels[i] = image['label']
