from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from create_dataset import create_dataset  # type: ignore
from helpers.s3 import save_json_file

OUTPUT_FILE = "dataset.json"


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
    output_data = {
        "images": images.tolist(),
        "labels": labels.tolist(),
        "uids": uids.tolist()
    }
    filename = f"dagster/runs/{context.run_id}/{OUTPUT_FILE}"
    save_json_file(output_data, filename)

    return MaterializeResult(
        metadata={
            "size": MetadataValue.int(len(images))
        }
    )
