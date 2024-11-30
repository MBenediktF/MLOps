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
    group_name="Training",
    kinds={"s3", "numpy"},
    description="Create dataset from measurements"
)
def dataset(
    context: AssetExecutionContext,
    config: DatasetCreateConfig
) -> MaterializeResult:

    # Run create dataset function from model code
    images, labels, uids = create_dataset(
        measurements=config.measurements,
        img_size=(None, config.img_height, config.img_width, 3),
        context=context
    )

    # store the dataset as json
    dataset_json = {
        "images": images.tolist(),
        "labels": labels.tolist(),
        "uids": uids.tolist()
    }
    dir = f"data/runs/{context.run_id}"
    os.makedirs(dir, exist_ok=True)
    with open(f"{dir}/dataset.json", "w") as f:
        json.dump(dataset_json, f)

    return MaterializeResult(
        metadata={
            "size": MetadataValue.int(len(images))
        }
    )
