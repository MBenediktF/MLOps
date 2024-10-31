def fit_model(
        model, x_train, y_train, optimizer, loss, metrics, epochs, batch_size):
    # Compile model
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # Fit model
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    return history
