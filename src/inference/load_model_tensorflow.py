import mlflow


def load_model(experiment: str, run_id: str):
    mlflow.set_experiment(experiment)

    try:
        model = mlflow.tensorflow.load_model(f"runs:/{run_id}/model")
    except Exception:
        raise Exception("Model could not be loaded")

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
