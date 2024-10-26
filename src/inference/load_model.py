import mlflow
import mlflow.tensorflow
from dotenv import load_dotenv
import os

load_dotenv()

mlflow_port = os.getenv('MLFLOW_PORT')
mlflow.set_tracking_uri(f"http://mlflow:{mlflow_port}")


def enable_local_dev():
    mlflow.set_tracking_uri(f"http://localhost:{mlflow_port}")


def load_model(experiment: str, run_id: str):
    mlflow.set_experiment(experiment)

    try:
        model = mlflow.tensorflow.load_model(f"runs:/{run_id}/model")
    except Exception as e:
        raise Exception(f"Model could not be loaded: {e}")

    return model


def load_model_with_best_accuracy(experiment: str):
    mlflow.set_experiment(experiment)

    try:
        runs = mlflow.search_runs(
            experiment, order_by=["metrics.accuracy DESC"], max_results=1
        )
        best_run_id = runs[0].info.run_id
        model = mlflow.tensorflow.load_model(f"runs:/{best_run_id}/model")
    except Exception:
        raise Exception("Model could not be loaded")

    return model


def load_registered_model(model_name: str, version: str = "latest"):
    try:
        model = mlflow.tensorflow.load_model(f"models:/{model_name}/{version}")
    except Exception as e:
        raise Exception(f"Model could not be loaded: {e}")

    return model
