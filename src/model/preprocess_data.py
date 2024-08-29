def preprocess_data(x_train, x_test):
    # Normalisierung der Daten
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    return x_train, x_test
