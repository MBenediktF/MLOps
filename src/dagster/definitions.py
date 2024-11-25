from assets.dataset import dataset
from assets.dataset_preprocessed import dataset_preprocessed
from assets.model import model
from assets.trained_model import trained_model
from assets.train_data import train_data
from assets.test_data import test_data

from dagster import Definitions

defs = Definitions(assets=[
    dataset,
    dataset_preprocessed,
    train_data,
    test_data,
    model,
    trained_model
    ])
