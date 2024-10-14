import mlflow
import mlflow.tensorflow

from model.import_dataset import import_dataset
from model.preprocess_data import preprocess_data
from model.create_model import create_model
from model.fit_model import fit_model
from model.evaluate_model import evaluate_model

mlflow_tracking_uri = "http://localhost:5003"
dataset_id = "ea93eb20-616c-4ad2-9d82-cca701766612"
experiment_name = "Experiment_1"
test_split = 0.2
dropout = 0.2
epochs = 5

mlflow.set_tracking_uri(mlflow_tracking_uri)


def main():
    # Daten importieren
    images, labels, uids = import_dataset(dataset_id)

    # Daten vorverarbeiten
    train_x, train_y, train_uids, test_x, test_y, test_uids = \
        preprocess_data(images, labels, uids, test_split)

    # Experiment erstellen
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        mlflow.tensorflow.autolog()

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
        mlflow.tensorflow.mlflow.log_param("dataset_id", dataset_id)

    mlflow.end_run()


if __name__ == "__main__":
    main()
