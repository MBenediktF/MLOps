import tensorflow as tf


def fit_model(model, x_train, y_train):
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])

    # Trainiere das Modell
    history = model.fit(x_train, y_train, epochs=5)

    return history
