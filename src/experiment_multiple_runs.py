import os
import tensorflow as tf
import certifi
import mlflow
import mlflow.tensorflow

from model.import_data import import_data
from model.preprocess_data import preprocess_data
from model.create_model import create_model
from model.fit_model import fit_model
from model.evaluate_model import evaluate_model

print("TensorFlow version:", tf.__version__)

os.environ['SSL_CERT_FILE'] = certifi.where()


def mlflow_run(x_train, y_train, x_test, y_test, dropout, epochs):
    with mlflow.start_run():

        mlflow.tensorflow.autolog()

        # Log the hyperparameters
        mlflow.log_param("dropout", dropout)
        mlflow.log_param("epochs", epochs)

        # Modell erstellen
        model = create_model(dropout=0.2)

        # Modell trainieren
        fit_model(model, x_train, y_train,
                  optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'],
                  epochs=epochs)

        # Modell evaluieren
        eval = evaluate_model(model, x_test, y_test)

        # Metriken loggen
        mlflow.tensorflow.mlflow.log_metric("evaluation_accuracy", eval[1])

    mlflow.end_run()


def main():
    # Daten importieren
    x_train, y_train, x_test, y_test = import_data()

    # Daten vorverarbeiten
    x_train, x_test = preprocess_data(x_train, x_test)

    # Define hyperparameter grid
    parameters = {
        'dropout': [0.2, 0.3],
        'epochs': [5, 10]
    }

    # Set experiment
    mlflow.set_experiment("MNIST Multiple Runs")

    # Iterate over all combinations of hyperparameters
    for dropout in parameters['dropout']:
        for epochs in parameters['epochs']:
            mlflow_run(x_train, y_train, x_test, y_test, dropout, epochs)


if __name__ == "__main__":
    main()
