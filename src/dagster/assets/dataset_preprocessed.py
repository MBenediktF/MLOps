import numpy as np
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import json
import os
from model.preprocess_data import preprocess_data  # type: ignore


class DatasetPreprocessingConfig(Config):
    test_split: float = 0.2
    seed: int = 0


@asset(
    deps=["dataset"],
    group_name="Training",
    kinds={"numpy", "scikitlearn"},
    description="Preprocessed, splitted dataset"
)
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
    dataset_uid = dataset["dataset_uid"]

    train_x, train_y, train_uids, test_x, test_y, test_uids = \
        preprocess_data(images, labels, uids, test_split, seed)

    dataset_json = {
        "train_x": train_x.tolist(),
        "train_y": train_y.tolist(),
        "train_uids": train_uids.tolist(),
        "test_x": test_x.tolist(),
        "test_y": test_y.tolist(),
        "test_uids": test_uids.tolist(),
        "dataset_uid": dataset_uid,
        "test_split": test_split,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/dataset_preprocessed.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size_train": MetadataValue.int(len(train_x)),
            "size_test": MetadataValue.int(len(test_x))
        }
    )
