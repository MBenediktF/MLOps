from src.model.create_model import create_model
import tensorflow as tf
import pytest


@pytest.mark.parametrize("dropout", [0.2, 0.8])
def test_create_model_valid(dropout):
    # check if the function returns a valid Keras model
    model = create_model(dropout=0.2)
    assert isinstance(model, tf.keras.Model), \
        "The returned model is not a Keras model"
    assert len(model.layers) > 0, \
        "The returned model has no layers"


@pytest.mark.parametrize("dropout", [-0.5, 1.2])
def test_create_model_invalid(dropout):
    # check how the funtion handles wrong dropout parameter
    with pytest.raises(ValueError):
        create_model(dropout=dropout)
