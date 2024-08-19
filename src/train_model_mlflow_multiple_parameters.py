
import os
import tensorflow as tf
import certifi
import mlflow
import mlflow.tensorflow


def start_mlflow_run(lr, dr, epochs):
    with mlflow.start_run():
        # Log the hyperparameters
        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("dropout_rate", dr)
        mlflow.log_param("epochs", epochs)

        # Build the model
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(dr),
            tf.keras.layers.Dense(10)
        ])

        # Compile the model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(
                from_logits=True
            ),
            metrics=['accuracy']
        )

        # Train the model
        model.fit(x_train, y_train, epochs=epochs, verbose=1)

        # Evaluate the model
        loss, accuracy = model.evaluate(x_test, y_test, verbose=2)

        # Log the metrics
        mlflow.log_metric("loss", loss)
        mlflow.log_metric("accuracy", accuracy)

        # Save the model as an artifact
        model_path = "model.h5"
        model.save(model_path)
        mlflow.log_artifact(model_path)

        mlflow.tensorflow.log_model(model, "model")

        mlflow.end_run()


# Set the SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Define hyperparameter grid
param_grid = {
    'learning_rate': [0.001, 0.01],
    'dropout_rate': [0.2, 0.3],
    'epochs': [5, 10]
}

# Start MLflow
mlflow.set_experiment("MNIST Hyperparameter Tuning")

# Iterate over all combinations of hyperparameters
for lr in param_grid['learning_rate']:
    for dr in param_grid['dropout_rate']:
        for epochs in param_grid['epochs']:
            start_mlflow_run(lr, dr, epochs)
