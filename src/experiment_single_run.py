import os
import tensorflow as tf
import certifi
import mlflow

from model.import_data import import_data
from model.preprocess_data import preprocess_data
from model.create_model import create_model
from model.fit_model import fit_model
from model.evaluate_model import evaluate_model

mlflow.autolog()

print("TensorFlow version:", tf.__version__)

os.environ['SSL_CERT_FILE'] = certifi.where()


def main():
    # Daten importieren
    x_train, y_train, x_test, y_test = import_data()

    # Daten vorverarbeiten
    x_train, x_test = preprocess_data(x_train, x_test)

    # Modell erstellen
    model = create_model()

    # Modell trainieren
    fit_model(model, x_train, y_train,
              optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'],
              epochs=5)

    # Modell evaluieren
    evaluate_model(model, x_test, y_test)

    # Modell speichern
    model.save('model.h5')


if __name__ == "__main__":
    main()
