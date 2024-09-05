from src.model.preprocess_data import preprocess_data
import tensorflow as tf
import pytest


@pytest.mark.parametrize("x_train, x_test", [(0, 255), (127, 127), (255, 0)])
def test_preprocess_data_valid(x_train, x_test):
    # check if the function returns a valid Keras model
    x_train, x_test = preprocess_data(x_train, x_test)
    assert isinstance(x_train, float), \
        "The returned x_train value is not a float"
    assert isinstance(x_test, float), \
        "The returned x_test value is not a float"
    assert x_train >= 0 and x_train <= 1, \
        "The returned x_train value is not between 0 and 1"
    assert x_test >= 0 and x_test <= 1, \
        "The returned x_test value is not between 0 and 1"


@pytest.mark.parametrize("x_train, x_test", [("", 0), (0, ""), ("", "")])
def test_preprocess_data_invalid(x_train, x_test):
    # check how the funtion handles wrong dropout parameter
    with pytest.raises(TypeError):
        x_train, x_test = preprocess_data(x_train, x_test)
