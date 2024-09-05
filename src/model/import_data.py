import pandas as pd
import os


def _load_mnist_from_csv(train_csv, test_csv):

    train_df = pd.read_csv(train_csv)
    test_df = pd.read_csv(test_csv)

    print(train_df.head())

    x_train = train_df.iloc[:, 1:].values
    y_train = train_df.iloc[:, 0].values

    x_test = test_df.iloc[:, 1:].values
    y_test = test_df.iloc[:, 0].values

    x_train = x_train.reshape(-1, 28, 28)
    x_test = x_test.reshape(-1, 28, 28)

    return x_train, y_train, x_test, y_test


def import_data():
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..'))
    train_csv_path = os.path.join(project_root, 'datasets', 'mnist_train.csv')
    test_csv_path = os.path.join(project_root, 'datasets', 'mnist_test.csv')
    x_train, y_train, x_test, y_test = _load_mnist_from_csv(
        train_csv_path,
        test_csv_path)
    return x_train, y_train, x_test, y_test
