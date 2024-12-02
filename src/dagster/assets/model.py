from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from model.create_model import create_model  # type: ignore
from helpers.s3 import save_model_file
import tempfile
from helpers.s3 import get_minio_filebrowser_url

OUTPUT_FILE = "model.h5"


class ModelConfig(Config):
    img_width: int = 100
    img_height: int = 75
    default_dropout: float = 0.2


@asset(
    group_name="Training",
    kinds={"tensorflow"},
    description="Untrained model architecture"
)
def model(
    context: AssetExecutionContext,
    config: ModelConfig
) -> MaterializeResult:
    # Get model parameters fro config
    img_width = config.img_width
    img_height = config.img_height
    dropout = config.default_dropout

    # Create model
    model = create_model((None, img_height, img_width, 3), dropout)
    context.log.info(f"Model summary: {model.summary()}")

    # Save the model as .h5 file
    with tempfile.TemporaryDirectory() as tempdir:
        temp_file_path = f"{tempdir}/{OUTPUT_FILE}"
        model.save(temp_file_path)
        filename = f"dagster/runs/{context.run_id}/{OUTPUT_FILE}"
        save_model_file(temp_file_path, filename)

    file_url = file_url = get_minio_filebrowser_url(filename)
    return MaterializeResult(
        metadata={
            "num_layers": MetadataValue.int(len(model.layers)),
            "num_parameters": MetadataValue.int(model.count_params()),
            "file": MetadataValue.url(file_url)
        }
    )
