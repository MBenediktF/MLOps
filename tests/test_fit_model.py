from src.model.fit_model import fit_model
import tensorflow as tf


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
              loss="sparse_categorical_crossentropy",
              metrics=['accuracy'],
              epochs=1)

    assert isinstance(model, tf.keras.Model), \
        "The trained model is not a Keras model"
