import tensorflow as tf
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # noqa: E501
from src.model.fit_model import fit_model  # noqa: E402


model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(shape=(4, 4)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])
x_train = tf.random.normal((10, 4, 4))
y_train = tf.random.uniform((10,), maxval=10, dtype=tf.int32)


def test_fit_model_valid():
    fit_model(model, x_train, y_train,
              optimizer='adam',
              loss="mse",
              metrics=['accuracy'],
              epochs=1,
              batch_size=1
              )

    assert isinstance(model, tf.keras.Model), \
        "The trained model is not a Keras model"
