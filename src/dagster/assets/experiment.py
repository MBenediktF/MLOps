import tensorflow as tf
from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import numpy as np
import os
from dotenv import load_dotenv
import mlflow
from model.fit_model import fit_model  # type: ignore
from model.evaluate_model import evaluate_model  # type: ignore
from helpers.logs import Log
from helpers.s3 import load_json_file, load_model_file, save_json_file
from helpers.s3 import get_minio_filebrowser_url
import tempfile

INPUT_MODEL = "model.h5"
INPUT_FILE = "dataset_preprocessed.json"
OUTPUT_FILE = "experiment.json"

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
        model_path,
        train_x, train_y, test_x, test_y,
        dropout, epochs, batch_size, test_split,
        optimizer, loss, metrics
        ):
    with mlflow.start_run():
        mlflow.tensorflow.autolog()

        # Log inputs
        mlflow.log_input(mlflow.data.from_numpy(
            features=train_x, targets=train_y), context="train")
        mlflow.log_input(mlflow.data.from_numpy(
            features=test_x, targets=test_y), context="test")

        # Load model
        model = tf.keras.models.load_model(model_path)

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
    model_from_run: str = ''
    preprocessed_dataset_from_run: str = ''


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

    dataset_run = config.preprocessed_dataset_from_run if config else None
    if not dataset_run:
        dataset_run = context.run_id
    model_run = config.model_from_run if config else None
    if not model_run:
        model_run = context.run_id

    # get preprocessed dataset from dataset_preprocessed
    input_data = load_json_file(f"dagster/runs/{dataset_run}/{INPUT_FILE}")
    train_x = np.array(input_data["train_x"])
    train_y = np.array(input_data["train_y"])
    test_x = np.array(input_data["test_x"])
    test_y = np.array(input_data["test_y"])
    test_split = input_data["test_split"]

    # Config experiment
    mlflow.set_experiment(config.name)
    experiment = mlflow.get_experiment_by_name(config.name)
    experiment_id = experiment.experiment_id

    tempdir = tempfile.TemporaryDirectory()
    model_path = f'{tempdir.name}/{INPUT_MODEL}'
    context.log.info(f"Model path: {model_path}")
    load_model_file(f'dagster/runs/{model_run}/{INPUT_MODEL}', model_path)

    # Iterate over all combinations of hyperparameters
    iter = len(config.dropout) * len(config.epochs) * len(config.batch_size)
    log.log(f"Experiment started, {iter} iterations to go")
    for dropout in config.dropout:
        for epochs in config.epochs:
            for batch_size in config.batch_size:
                log.log(f"Running experiment with dropout: {dropout}, " +
                        f"epochs: {epochs}, batch_size: {batch_size}")
                mlflow_run(
                    model_path,
                    train_x, train_y, test_x, test_y,
                    dropout, epochs, batch_size,
                    test_split,
                    config.optimizer,
                    config.loss,
                    config.metrics
                )
    log.log("Experiment finished")

    # store experiment metadata
    output_data = {
        "name": config.name,
        "id": experiment_id
    }
    filename = f"dagster/runs/{context.run_id}/{OUTPUT_FILE}"
    save_json_file(output_data, filename)

    experiment_url = f"{mlflow_url}/experiments/{experiment_id}"
    file_url = file_url = get_minio_filebrowser_url(filename)
    return MaterializeResult(
        metadata={
            "iterations": MetadataValue.int(iter),
            "experiment": MetadataValue.url(experiment_url),
            "id": MetadataValue.text(experiment_id),
            "file": MetadataValue.url(file_url)
        }
    )
