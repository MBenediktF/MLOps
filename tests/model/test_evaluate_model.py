import tensorflow as tf
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # noqa: E501
from src.model.evaluate_model import evaluate_model  # noqa: E402


model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(shape=(4, 4)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])
x_test = tf.random.normal((10, 4, 4))
y_test = tf.random.uniform((10,), maxval=10, dtype=tf.int32)


def test_evaluate_model_valid():
    model.compile(optimizer="adam", loss="mse", metrics=['accuracy'])
    test_loss, test_acc = evaluate_model(model, x_test, y_test)
    assert isinstance(test_loss, float), \
        "The returned loss is not a float"
    assert isinstance(test_acc, float), \
        "The returned accuracy is not a float"
