from src.model.create_model import create_model
import tensorflow as tf
import pytest


def test_create_model():
    # check if the function returns a valid Keras model
    model = create_model(dropout=0.2)
    assert isinstance(model, tf.keras.Model), "The returned model is not a Keras model"
    assert len(model.layers) > 0, "The returned model has no layers"

    # check how the funtion handles wrong dropout parameter
    with pytest.raises(ValueError):
        model = create_model(dropout=-0.5)
    with pytest.raises(ValueError):
        model = create_model(dropout=1.2)
