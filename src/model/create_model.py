import tensorflow as tf


def create_model(dropout=0.2):
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(shape=(28, 28)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(10)
    ])
    return model
