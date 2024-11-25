import numpy as np
import json
import os
from dagster import AssetExecutionContext
from dagster import asset, MaterializeResult


@asset(
    deps=["dataset_preprocessed"],
    group_name=None,
    kinds={"numpy"},
    description="Training dataset"
)
def train_data(
    context: AssetExecutionContext,
) -> MaterializeResult:

    with open("data/dataset_preprocessed.json", "r") as f:
        dataset = json.load(f)

    images = np.array(dataset["train_x"])
    labels = np.array(dataset["train_y"])
    uids = np.array(dataset["train_uids"])

    # store the dataset as json
    dataset_json = {
        "images": images.tolist(),
        "labels": labels.tolist(),
        "uids": uids.tolist()
    }
    os.makedirs("data", exist_ok=True)
    with open("data/train_data.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size": len(images),
        }
    )
