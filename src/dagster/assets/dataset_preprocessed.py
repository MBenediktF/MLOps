import numpy as np
from sklearn.utils import shuffle
from dagster import AssetExecutionContext, Definitions
from dagster import asset, Config, MaterializeResult, Failure
import json
import os


class DatasetPreprocessingConfig(Config):
    test_split: float = 0.2
    seed: int = 0


@asset(deps=["dataset"])
def dataset_preprocessed(
    context: AssetExecutionContext,
    config: DatasetPreprocessingConfig
) -> MaterializeResult:
    test_split = config.test_split if config else 0.2
    seed = config.seed if config else 0

    # get dataset from import_dataset
    with open("data/dataset.json", "r") as f:
        dataset = json.load(f)

    images = np.array(dataset["images"])
    labels = np.array(dataset["labels"])
    uids = np.array(dataset["uids"])

    # Check input data
    if np.any(images < 0) or np.any(images > 255):
        raise Failure("Input data must be between 0 and 255")

    if uids is None:
        uids = np.arange(images.shape[0])

    # Normalize features
    images = images / 255.0

    # Normalize labels
    labels = np.clip(labels, 0, 250)
    labels = np.round(labels / 250.0, 2)

    # shuffle dataset
    images, labels, uids = shuffle(images, labels, uids, random_state=seed)

    # split dataset
    index = round(images.shape[0] * test_split)
    test_x, test_y, test_uids = images[0:index], labels[0:index], uids[0:index]
    train_x, train_y, train_uids = images[index:], labels[index:], uids[index:]

    dataset_json = {
        "train_x": train_x.tolist(),
        "train_y": train_y.tolist(),
        "train_uids": train_uids.tolist(),
        "test_x": test_x.tolist(),
        "test_y": test_y.tolist(),
        "test_uids": test_uids.tolist()
    }
    os.makedirs("data", exist_ok=True)
    with open("data/dataset_preprocessed.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size_train": len(train_x),
            "size_test": len(test_x)
        }
    )


defs = Definitions(assets=[dataset_preprocessed])
