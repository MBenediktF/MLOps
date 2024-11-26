import json
import os
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from model.import_dataset import import_dataset  # type: ignore


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

    # check config options
    if config.use_latest:
        # get dataset uid from new_dataset json
        with open("data/new_dataset.json", "r") as f:
            new_dataset_metadata = json.load(f)
            dataset_uid = new_dataset_metadata["uid"]
    else:
        dataset_uid = config.dataset_uid

    # load and comvert dataset
    images, labels, uids = import_dataset(dataset_uid)

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
