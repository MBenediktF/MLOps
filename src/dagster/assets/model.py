from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
from model.create_model import create_model  # type: ignore
import os


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
    dir = f"data/runs/{context.run_id}"
    os.makedirs(dir, exist_ok=True)
    model_path = f"{dir}/model.h5"
    model.save(model_path)

    return MaterializeResult(
        metadata={
            "num_layers": MetadataValue.int(len(model.layers)),
            "num_parameters": MetadataValue.int(model.count_params())
        }
    )
