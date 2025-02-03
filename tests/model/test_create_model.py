import pytest
import tensorflow as tf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # noqa: E501
from src.model.create_model import create_model  # noqa: E402

img_size = (None, 75, 100, 3)


@pytest.mark.parametrize("dropout", [0.2, 0.8])
def test_create_model_valid(dropout):
    model = create_model(img_size, dropout=dropout)
    assert isinstance(model, tf.keras.Model), \
        "The returned model is not a Keras model"
    assert len(model.layers) > 0, \
        "The returned model has no layers"


@pytest.mark.parametrize("dropout", [-0.5, 1.2])
def test_create_model_valueerr(dropout):
    with pytest.raises(ValueError):
        create_model(img_size, dropout=dropout)


@pytest.mark.parametrize("dropout", ["", (), None])
def test_create_model_typeerr(dropout):
    with pytest.raises(TypeError):
        create_model(img_size, dropout=dropout)
