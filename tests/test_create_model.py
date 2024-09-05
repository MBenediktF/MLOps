from src.model.create_model import create_model


def test_create_model():
    model = create_model(dropout=0.2)
    assert model is not None
