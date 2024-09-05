from src.model.import_data import import_data
from unittest import mock
import numpy as np
import pandas as pd


@mock.patch('src.model.import_data.pd.read_csv',
            return_value=pd.read_csv('tests/mock_data.csv'))
def test_import_data(mocked_data):
    x_train, y_train, x_test, y_test = import_data()
    print(type(x_train))
    assert isinstance(x_train, np.ndarray), \
        "The returned x_train object are not a numpy ndarray"
    assert isinstance(y_train, np.ndarray), \
        "The returned y_train object are not a numpy ndarray"
    assert isinstance(x_test, np.ndarray), \
        "The returned x_test object are not a numpy ndarray"
    assert isinstance(y_test, np.ndarray), \
        "The returned y_test object are not a numpy ndarray"
