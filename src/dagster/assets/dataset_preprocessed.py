import numpy as np
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from model.preprocess_data import preprocess_data  # type: ignore
from helpers.s3 import save_json_file, load_json_file

INPUT_FILE = "dataset.json"
OUTPUT_FILE = "dataset_preprocessed.json"


class DatasetPreprocessingConfig(Config):
    test_split: float = 0.2
    seed: int = 0
    dataset_from_run: str = ''


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

    # get config values
    test_split = config.test_split if config else 0.2
    seed = config.seed if config else 0
    run = config.dataset_from_run if config else None

    if not run:
        run = context.run_id

    # get dataset from json file
    input_data = load_json_file(f"dagster/runs/{run}/{INPUT_FILE}")
    images = np.array(input_data["images"])
    labels = np.array(input_data["labels"])
    uids = np.array(input_data["uids"])

    if len(images) == 0:
        raise ValueError("Dataset is empty")

    # run preprocess data script
    train_x, train_y, train_uids, test_x, test_y, test_uids = \
        preprocess_data(images, labels, uids, test_split, seed)

    # save new dataset
    output_data = {
        "train_x": train_x.tolist(),
        "train_y": train_y.tolist(),
        "train_uids": train_uids.tolist(),
        "test_x": test_x.tolist(),
        "test_y": test_y.tolist(),
        "test_uids": test_uids.tolist(),
        "test_split": test_split,
    }
    filename = f"dagster/runs/{context.run_id}/{OUTPUT_FILE}"
    save_json_file(output_data, filename)

    return MaterializeResult(
        metadata={
            "size_train": MetadataValue.int(len(train_x)),
            "size_test": MetadataValue.int(len(test_x))
        }
    )
