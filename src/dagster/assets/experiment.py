import tensorflow as tf
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import json
import numpy as np
import os
from dotenv import load_dotenv
import mlflow
from model.fit_model import fit_model  # type: ignore
from model.evaluate_model import evaluate_model  # type: ignore
from helpers.logs import Log

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
host = os.getenv('HOST')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")
mlflow_url = f"{host}:{mlflow_port}/#"


def update_dropout_layers(model, dropout):
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Dropout):
            layer.rate = dropout


def mlflow_run(
        train_x, train_y, test_x, test_y,
        dropout, epochs, batch_size, test_split,
        dataset_id, optimizer, loss, metrics
        ):
    with mlflow.start_run():
        mlflow.tensorflow.autolog()

        # Log inputs
        mlflow.tensorflow.mlflow.log_param("dataset_id", dataset_id)
        mlflow.log_input(mlflow.data.from_numpy(
            features=train_x, targets=train_y), context="train")
        mlflow.log_input(mlflow.data.from_numpy(
            features=test_x, targets=test_y), context="test")

        # Load model
        model = tf.keras.models.load_model("data/model.h5")

        # Set dropouts
        update_dropout_layers(model, dropout)

        # Model training
        fit_model(
            model,
            train_x,
            train_y,
            optimizer,
            loss,
            metrics,
            epochs,
            batch_size
        )

        # Modell evaluieren
        test_loss, test_mae = evaluate_model(model, test_x, test_y)

        # Metriken loggen
        mlflow.tensorflow.mlflow.log_metric("test_loss", test_loss)
        mlflow.tensorflow.mlflow.log_metric("test_mae", test_mae)
        mlflow.tensorflow.mlflow.log_param("dropout", dropout)
        mlflow.tensorflow.mlflow.log_param("test_split", test_split)
        mlflow.tensorflow.mlflow.log_param("epochs", epochs)
        mlflow.tensorflow.mlflow.log_param("batch_size", batch_size)

        tf.keras.backend.clear_session()

    mlflow.end_run()


class ExperimentConfig(Config):
    name: str = ""
    optimizer: str = "adam"
    loss: str = "mean_squared_error"
    metrics: list = ["mae"]
    epochs: list = [10]
    batch_size: list = [32]
    dropout: list = [0.2]


@asset(
    deps=["dataset_preprocessed", "model"],
    group_name="Training",
    kinds={"tensorflow", "mlflow"},
    description="Run MLFlow experiment"
)
def experiment(
    context: AssetExecutionContext,
    config: ExperimentConfig
) -> MaterializeResult:
    log = Log(context)

    # get preprocessed dataset from dataset_preprocessed
    with open("data/dataset_preprocessed.json", "r") as f:
        dataset = json.load(f)
    train_x = np.array(dataset["train_x"])
    train_y = np.array(dataset["train_y"])
    test_x = np.array(dataset["test_x"])
    test_y = np.array(dataset["test_y"])
    dataset_uid = dataset["dataset_uid"]
    test_split = dataset["test_split"]

    # Config experiment
    mlflow.set_experiment(config.name)
    experiment = mlflow.get_experiment_by_name(config.name)
    experiment_id = experiment.experiment_id

    # Iterate over all combinations of hyperparameters
    iter = len(config.dropout) * len(config.epochs) * len(config.batch_size)
    log.log(f"Experiment started, {iter} iterations to go")
    for dropout in config.dropout:
        for epochs in config.epochs:
            for batch_size in config.batch_size:
                log.log(f"Running experiment with dropout: {dropout},\
                         epochs: {epochs}, batch_size: {batch_size}")
                mlflow_run(
                    train_x, train_y, test_x, test_y,
                    dropout, epochs, batch_size,
                    dataset_uid, test_split,
                    config.optimizer,
                    config.loss,
                    config.metrics
                )
    log.log("Experiment finished")

    # store experiment metadata
    experiment_json = {
        "name": config.name,
        "id": experiment_id
    }
    os.makedirs("data", exist_ok=True)
    with open("data/experiment.json", "w") as f:
        json.dump(experiment_json, f)

    experiment_url = f"{mlflow_url}/experiments/{experiment_id}"
    return MaterializeResult(
        metadata={
            "iterations": MetadataValue.int(iter),
            "experiment": MetadataValue.url(experiment_url),
            "id": MetadataValue.text(experiment_id)
        }
    )
