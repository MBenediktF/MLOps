import tensorflow as tf
from dagster import AssetExecutionContext
from dagster import asset, Config, MaterializeResult
import json
import numpy as np


class TrainingConfig(Config):
    optimizer: str = "adam"
    loss: str = "mean_squared_erro"
    metrics: list = ["mae"]
    epochs: int = 10
    batch_size: int = 32


@asset(deps=["dataset_preprocessed", "model"], group_name=None)
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
    with open("data/dataset_preprocessed.json", "r") as f:
        dataset = json.load(f)
    x_train = np.array(dataset["train_x"])
    y_train = np.array(dataset["train_y"])

    # get model from model
    model = tf.keras.models.load_model("data/model.h5")

    # Compile model
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # Fit model
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    return MaterializeResult(
        metadata={
            history: history.history
        }
    )
