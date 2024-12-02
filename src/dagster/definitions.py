from assets.dataset import dataset
from assets.dataset_preprocessed import dataset_preprocessed
from assets.model import model
from assets.experiment import experiment
from assets.best_run import best_run
from assets.registered_model import registered_model
from jobs.training import training_job
from jobs.training_register import training_register_job
from dagster import Definitions


defs = Definitions(
    assets=[
        dataset,
        dataset_preprocessed,
        model,
        experiment,
        best_run,
        registered_model
    ],
    jobs=[
        training_job,
        training_register_job
    ]
)
