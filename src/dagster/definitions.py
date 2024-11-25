from assets.dataset import dataset
from assets.dataset_preprocessed import dataset_preprocessed
from assets.model import model
from assets.trained_model import trained_model

from dagster import Definitions

defs = Definitions(assets=[
    dataset,
    dataset_preprocessed,
    model, trained_model
    ])
