from dagster import AssetExecutionContext, MetadataValue
from dagster import asset, Config, MaterializeResult
import os
from dotenv import load_dotenv
import mlflow
from mlflow.tracking import MlflowClient
from helpers.s3 import load_json_file

INPUT_FILE = "best_run.json"

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
host = os.getenv('HOST')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")
mlflow_url = f"{host}:{mlflow_port}/#"


class RegisterConfig(Config):
    model_name: str = ""
    best_run_from_run: str = ''


@asset(
    deps=["best_run"],
    group_name="Register",
    kinds={"mlflow"},
    description="Register model in MLflow"
)
def registered_model(
    context: AssetExecutionContext,
    config: RegisterConfig
) -> MaterializeResult:

    run = config.best_run_from_run
    if not run:
        run = context.run_id

    # get run metadata
    input_data = load_json_file(f"dagster/runs/{run}/{INPUT_FILE}")
    run_id = input_data["id"]

    # register model
    model_version = None
    model_uri = f"runs:/{run_id}/model"
    client = MlflowClient()
    model_version = client.create_model_version(
        name=config.model_name,
        source=model_uri,
        run_id=run_id,
        tags={"auto": ""}
    )

    model_url = f"{mlflow_url}/models/{config.model_name}"
    version = model_version.version if model_version else "Not registered"
    return MaterializeResult(
        metadata={
            "model": MetadataValue.url(model_url),
            "new_model_version": MetadataValue.text(version)
        }
    )
