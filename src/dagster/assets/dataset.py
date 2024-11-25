from helpers.s3 import download_dataset
import numpy as np
from io import BytesIO
from PIL import Image
import json
import os
from dagster import AssetExecutionContext
from dagster import asset, Config, MaterializeResult, Failure


class DatasetImportConfig(Config):
    dataset_uid: str = ""


@asset(group_name=None)
def dataset(
    context: AssetExecutionContext,
    config: DatasetImportConfig
) -> MaterializeResult:

    dataset = download_dataset(config.dataset_uid)
    if not dataset:
        raise Failure("Could not download dataset")

    # get image width and height
    first_image = next(iter(dataset.values()))
    img_width, img_height = Image.open(BytesIO(first_image)).size

    # restructure dataset
    images = np.zeros((len(dataset), img_height, img_width, 3), dtype=np.uint8)
    labels = np.zeros((len(dataset)), dtype=np.uint16)
    uids = np.zeros((len(dataset)), dtype='U36')
    for i, (filename, image) in enumerate(dataset.items()):
        try:
            images[i] = np.array(Image.open(BytesIO(image)))
        except Exception as e:
            context.log.info(f"Could not read image: {e}")
            continue
        labels[i] = int(filename.split('_')[-1].split('.')[0])
        uids[i] = filename.split('/')[2].split('_')[0]

    # store the dataset as json
    dataset_json = {
        "images": images.tolist(),
        "labels": labels.tolist(),
        "uids": uids.tolist()
    }
    os.makedirs("data", exist_ok=True)
    with open("data/dataset.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size": len(images),
        }
    )
