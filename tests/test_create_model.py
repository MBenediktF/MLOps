from src.model.create_model import create_model
import tensorflow as tf


def test_create_model():
    model = create_model(dropout=0.2)
    assert isinstance(model, tf.keras.Model), "The returned model is not a Keras model"
    assert len(model.layers) > 0, "The returned model has no layers"
