from assets.dataset import dataset
from assets.dataset_preprocessed import dataset_preprocessed
from assets.model import model
from assets.trained_model import trained_model

from dagster import Definitions, AssetGroup

training_assets = AssetGroup(
    name="training",
    assets=[dataset, dataset_preprocessed, model, trained_model]
)

defs = Definitions(asset_groups=[
    training_assets
    ])
