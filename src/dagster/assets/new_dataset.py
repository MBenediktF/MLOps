import json
import os
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from create_dataset import create_dataset  # type: ignore


class DatasetCreateConfig(Config):
    measurements: list = [""]
    img_width: int = 100
    img_height: int = 75


@asset(
    group_name="Dataset",
    kinds={"s3", "numpy"},
    description="Create new dataset from measurements"
)
def new_dataset(
    context: AssetExecutionContext,
    config: DatasetCreateConfig
) -> MaterializeResult:

    # Run create dataset function from model code
    images, labels, uids = create_dataset(
        measurements=config.measurements,
        img_size=(None, config.img_height, config.img_width, 3),
        context=context
    )

    new_dataset_json = {
        "size": len(images)
    }
    os.makedirs("data", exist_ok=True)
    with open("data/new_dataset.json", "w") as f:
        json.dump(new_dataset_json, f)

    return MaterializeResult(
        metadata={
            "size": MetadataValue.int(len(images))
        }
    )
