import mlflow
import mlflow.tensorflow

from import_dataset import import_dataset
from preprocess_data import preprocess_data
from create_model import create_model
from fit_model import fit_model
from evaluate_model import evaluate_model

from dotenv import load_dotenv
import os

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")


def enable_local_dev():
    mlflow.set_tracking_uri(f"http://localhost:{mlflow_port}")


def mlflow_run(
        train_x, train_y, test_x, test_y,
        dropout, epochs, batch_size, test_split,
        dataset_id, dataset_train, dataset_test
        ):
    with mlflow.start_run():
        mlflow.tensorflow.autolog()

        # Log inputs
        mlflow.log_input(dataset_train, context="train")
        mlflow.log_input(dataset_test, context="test")

        # Modell erstellen
        model = create_model(test_x.shape, dropout)

        # Modell trainieren
        fit_model(model, train_x, train_y,
                  optimizer='adam',
                  loss="mean_squared_error",
                  metrics=['mae'],
                  epochs=epochs,
                  batch_size=batch_size
                  )

        # Modell evaluieren
        test_loss, test_acc = evaluate_model(model, test_x, test_y)

        # Metriken loggen
        mlflow.tensorflow.mlflow.log_metric("test_loss", test_loss)
        mlflow.tensorflow.mlflow.log_metric("test_loss", test_acc)
        mlflow.tensorflow.mlflow.log_param("dropout", dropout)
        mlflow.tensorflow.mlflow.log_param("test_split", test_split)
        mlflow.tensorflow.mlflow.log_param("epochs", epochs)
        mlflow.tensorflow.mlflow.log_param("batch_size", batch_size)
        mlflow.tensorflow.mlflow.log_param("dataset_id", dataset_id)

    mlflow.end_run()


def check_parameter_grid(parameters):
    # Check if parameters exists and is a dictionary
    if not isinstance(parameters, dict):
        raise ValueError("The 'parameters' variable must be a dictionary.")

    # Check if the keys 'dropout' and 'epochs' exist
    required_keys = ['dropout', 'epochs']
    for key in required_keys:
        if key not in parameters:
            raise KeyError(f"The key '{key}' is missing from 'parameters'.")

    # Check if the values associated with the keys are lists
    for key in required_keys:
        if not isinstance(parameters[key], list):
            raise ValueError(f"The value of '{key}' must be a list.")


def run_experiment(experiment_name, dataset_id, test_split, parameters):
    # Daten importieren
    images, labels, _ = import_dataset(dataset_id)

    # Daten vorverarbeiten
    train_x, train_y, _, test_x, test_y, _ = \
        preprocess_data(images, labels, _, test_split)

    dataset_train = mlflow.data.from_numpy(features=train_x, targets=train_y)
    dataset_test = mlflow.data.from_numpy(features=test_x, targets=test_y)

    # Set experiment
    mlflow.set_experiment(experiment_name)

    # Iterate over all combinations of hyperparameters
    for dropout in parameters['dropout']:
        for epochs in parameters['epochs']:
            for batch_size in parameters['batch_size']:
                mlflow_run(
                    train_x, train_y, test_x, test_y,
                    dropout, epochs, batch_size, test_split,
                    dataset_id, dataset_train, dataset_test
                )


if __name__ == "__main__":
    enable_local_dev()
    experiment_name = "Default"
    dataset_id = "ea93eb20-616c-4ad2-9d82-cca701766612"
    test_split = 0.2
    parameters = {
        'dropout': [0.2, 0.3],
        'epochs': [20],
        'batch_size': [64, 128]
    }
    run_experiment(experiment_name, dataset_id, test_split, parameters)
