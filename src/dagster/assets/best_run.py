from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import os
import json
from dotenv import load_dotenv
import mlflow

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
host = os.getenv('HOST')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")
mlflow_url = f"{host}:{mlflow_port}/#"


class BestRunConfig(Config):
    compare_metric: str = "test_mae"


@asset(
    deps=["experiment"],
    group_name="Training",
    kinds={"mlflow"},
    description="Best run from experiment"
)
def best_run(
    context: AssetExecutionContext,
    config: BestRunConfig
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

    # store run metadata
    run_json = {
        "id": best_run_id
    }
    os.makedirs("data", exist_ok=True)
    with open("data/best_run.json", "w") as f:
        json.dump(run_json, f)

    run_url = f"{mlflow_url}/experiments/{experiment_id}/runs/{best_run_id}"
    return MaterializeResult(
        metadata={
            "run": MetadataValue.url(run_url),
            "id": MetadataValue.text(best_run_id),
        }
    )
