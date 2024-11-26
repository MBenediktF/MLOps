from helpers.s3 import download_dataset
import numpy as np
from io import BytesIO
from PIL import Image
import json
import os
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult, Failure


class DatasetImportConfig(Config):
    use_latest: bool = False
    dataset_uid: str = ""


@asset(
    deps=["new_dataset"],
    group_name="Training",
    kinds={"s3"},
    description="Raw dataset from S3"
)
def dataset(
    context: AssetExecutionContext,
    config: DatasetImportConfig
) -> MaterializeResult:

    if config.use_latest:
        # get dataset uid from new_dataset json
        with open("data/new_dataset.json", "r") as f:
            new_dataset_metadata = json.load(f)
            dataset_uid = new_dataset_metadata["uid"]
    else:
        dataset_uid = config.dataset_uid

    dataset = download_dataset(dataset_uid)
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
        "uids": uids.tolist(),
        "dataset_uid": config.dataset_uid
    }
    os.makedirs("data", exist_ok=True)
    with open("data/dataset.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size": MetadataValue.int(len(images))
        }
    )
