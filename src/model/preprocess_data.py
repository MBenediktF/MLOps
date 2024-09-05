def preprocess_data(x_train, x_test):
    # Check input data
    if x_train < 0 or x_train > 255 or x_test < 0 or x_test > 255:
        raise ValueError("Input data must be between 0 and 255")

    # Normalize data
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    return x_train, x_test
