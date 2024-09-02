import pandas as pd


def load_mnist_from_csv(train_csv, test_csv):

    train_df = pd.read_csv(train_csv)
    test_df = pd.read_csv(test_csv)

    x_train = train_df.iloc[:, 1:].values
    y_train = train_df.iloc[:, 0].values

    x_test = test_df.iloc[:, 1:].values
    y_test = test_df.iloc[:, 0].values

    x_train = x_train.reshape(-1, 28, 28)
    x_test = x_test.reshape(-1, 28, 28)

    return x_train, y_train, x_test, y_test


def import_data():
    x_train, y_train, x_test, y_test = load_mnist_from_csv(
        '../datasets/mnist_train.csv',
        '../datasets/mnist_test.csv')
    return x_train, y_train, x_test, y_test
