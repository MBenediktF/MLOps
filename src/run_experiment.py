import mlflow
import mlflow.tensorflow

from model.import_dataset import import_dataset
from model.preprocess_data import preprocess_data
from model.create_model import create_model
from model.fit_model import fit_model
from model.evaluate_model import evaluate_model

mlflow.set_tracking_uri("http://localhost:5003")
dataset_id = "ea93eb20-616c-4ad2-9d82-cca701766612"
experiment_name = "Default"
test_split = 0.2


def mlflow_run(train_x, train_y, test_x, test_y,
               dropout, epochs,
               dataset_train, dataset_test):
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
                  metrics=['accuracy'],
                  epochs=epochs)

        # Modell evaluieren
        test_loss, test_acc = evaluate_model(model, test_x, test_y)

        # Metriken loggen
        mlflow.tensorflow.mlflow.log_metric("test_loss", test_loss)
        mlflow.tensorflow.mlflow.log_metric("test_loss", test_acc)
        mlflow.tensorflow.mlflow.log_param("dropout", dropout)
        mlflow.tensorflow.mlflow.log_param("test_split", test_split)
        mlflow.tensorflow.mlflow.log_param("epochs", epochs)
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


def run_experiment():
    # Daten importieren
    images, labels, _ = import_dataset(dataset_id)

    # Daten vorverarbeiten
    train_x, train_y, _, test_x, test_y, _ = \
        preprocess_data(images, labels, _, test_split)

    dataset_train = mlflow.data.from_numpy(features=train_x, targets=train_y)
    dataset_test = mlflow.data.from_numpy(features=test_x, targets=test_y)

    # Define hyperparameter grid
    parameters = {
        'dropout': [0.2, 0.3],
        'epochs': [3, 6]
    }

    # Set experiment
    mlflow.set_experiment(experiment_name)

    # Iterate over all combinations of hyperparameters
    for dropout in parameters['dropout']:
        for epochs in parameters['epochs']:
            mlflow_run(train_x, train_y, test_x, test_y,
                       dropout, epochs,
                       dataset_train, dataset_test
                       )


if __name__ == "__main__":
    experiment_name = "Default"
    dataset_id = "ea93eb20-616c-4ad2-9d82-cca701766612"
    test_split = 0.2
    parameters = {
        'dropout': [0.2, 0.3],
        'epochs': [3, 6]
    }
    run_experiment(experiment_name, dataset_id, test_split, parameters)
