import tensorflow as tf
from dagster import AssetExecutionContext
from dagster import asset, Config, MaterializeResult
import json
import numpy as np
import os


class TrainingConfig(Config):
    optimizer: str = "adam"
    loss: str = "mean_squared_error"
    metrics: list = ["mae"]
    epochs: int = 10
    batch_size: int = 32


@asset(
    deps=["train_data", "model"],
    group_name=None,
    kinds={"tensorflow"},
    description="Trained model"
)
def trained_model(
    context: AssetExecutionContext,
    config: TrainingConfig
) -> MaterializeResult:
    optimizer = config.optimizer
    loss = config.loss
    metrics = config.metrics
    epochs = config.epochs
    batch_size = config.batch_size

    # get preprocessed dataset from dataset_preprocessed
    with open("data/train_data.json", "r") as f:
        dataset = json.load(f)
    images = np.array(dataset["images"])
    labels = np.array(dataset["labels"])

    # get model from model
    model = tf.keras.models.load_model("data/model.h5")

    # Compile model
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # Fit model
    model.fit(images, labels, epochs=epochs, batch_size=batch_size)

    # Save the model as .h5 file
    os.makedirs("data", exist_ok=True)
    model_path = "data/model.h5"
    model.save(model_path)

    return MaterializeResult(
        metadata={}
    )
