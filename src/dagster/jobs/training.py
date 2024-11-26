from dagster import define_asset_job

training_job = define_asset_job(
    name="Training",
    selection=["dataset", "dataset_preprocessed", "model", "experiment"],
    config={
        "ops": {
            "dataset": {
                "config": {
                    "dataset_uid": "",
                    "use_latest": False
                }
            },
            "dataset_preprocessed": {
                "config": {
                    "seed": 0,
                    "test_split": 0.2
                }
            },
            "experiment": {
                "config": {
                    "batch_size": [32],
                    "dropout": [0.2],
                    "epochs": [10],
                    "loss": "mean_squared_error",
                    "metrics": ["mae"],
                    "name": "",
                    "optimizer": "adam"
                }
            },
            "model": {
                "config": {
                    "default_dropout": 0.2,
                    "img_height": 75,
                    "img_width": 100
                }
            },
            "best_run": {
                "config": {
                    "compare_metric": "test_mae"
                }
            }
        }
    }
)
