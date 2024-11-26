import json
import os
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from create_dataset import create_dataset_from_measurements  # type: ignore


class DatasetCreateConfig(Config):
    measurements: list = [""]


@asset(
    group_name="Dataset",
    kinds={"s3"},
    description="Create new dataset from measurements"
)
def new_dataset(
    context: AssetExecutionContext,
    config: DatasetCreateConfig
) -> MaterializeResult:

    dataset_uid, num_records = create_dataset_from_measurements(
        config.measurements,
        context
    )

    new_dataset_json = {
        "size": num_records,
        "uid": dataset_uid
    }
    os.makedirs("data", exist_ok=True)
    with open("data/new_dataset.json", "w") as f:
        json.dump(new_dataset_json, f)

    return MaterializeResult(
        {
            "size": MetadataValue.int(num_records),
            "uid": MetadataValue.text(dataset_uid)
        }
    )
