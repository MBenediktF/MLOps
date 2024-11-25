from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import os
import json
from dotenv import load_dotenv
import mlflow
from mlflow.tracking import MlflowClient

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
host = os.getenv('HOST')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")
mlflow_url = f"{host}:{mlflow_port}/#"


class RegisterConfig(Config):
    auto: bool = True
    model_name: str = ""
    compare_metric: str = "test_mae"


@asset(
    deps=["experiment"],
    group_name="Training",
    kinds={"mlflow"},
    description="Run MLFlow experiment"
)
def registered_model(
    context: AssetExecutionContext,
    config: RegisterConfig
) -> MaterializeResult:
    # get experiment and runs
    with open("data/experiment.json", "r") as f:
        experiment_metadata = json.load(f)
    experiment_id = experiment_metadata["id"]
    runs = mlflow.search_runs(experiment_id)

    # select best run by metric
    metric_str = f"metrics.{config.compare_metric}"
    best_run = runs.loc[runs[metric_str].idxmin()]
    best_run_id = best_run["run_id"]

    # register model
    if config.auto:
        model_uri = f"runs:/{best_run_id}/model"
        client = MlflowClient()
        client.create_model_version(
            name=config.model_name,
            source=model_uri,
            run_id=best_run_id,
        )

    run_url = f"{mlflow_url}/experiments/{experiment_id}/runs/{best_run_id}"
    model_url = f"{mlflow_url}/models/{config.model_name}"
    return MaterializeResult(
        metadata={
            "best_run": MetadataValue.text(best_run_id),
            "run": MetadataValue.url(run_url),
            "model": MetadataValue.url(model_url)
        }
    )
