import threading
import requests
import os
from dotenv import load_dotenv

load_dotenv()
dagster_port = os.getenv("DAGSTER_PORT")

dagster_api_url = f"http://dagster:{dagster_port}/graphql"


def trigger_retraining():
    thread = threading.Thread(target=send_api_request)
    thread.start()
    return


def send_api_request():
    # TODO: Dynamically set inputs, parameters, exp_name and model_name
    graphql_query = """
        mutation {
            launchPipelineExecution(
                executionParams: {
                    selector: {
                        repositoryLocationName: "definitions.py",
                        repositoryName: "__repository__",
                        jobName: "Train_and_Register"
                    },
                    runConfigData: {
                        ops: {
                            best_run: {
                                config: {
                                    compare_metric: "test_mae"
                                }
                            },
                            dataset: {
                                config: {
                                    img_height: 75,
                                    img_width: 100,
                                    measurements: ["env_beige_distant", "val_env_beige_distant", "val_env_beige_default+distant", "test_retraining_trigger"],
                                }
                            },
                            dataset_preprocessed: {
                                config: {
                                    seed: 0,
                                    test_split: 0.2
                                }
                            },
                            experiment: {
                                config: {
                                    batch_size: [64, 128],
                                    dropout: [0.1, 0.15],
                                    epochs: [100],
                                    loss: "mean_squared_error",
                                    metrics: ["mae"],
                                    name: "alert-triggered-retraining",
                                    optimizer: "adam"
                                }
                            },
                            model: {
                                config: {
                                    default_dropout: 0.2,
                                    img_height: 75,
                                    img_width: 100
                                }
                            },
                            registered_model: {
                                config: {
                                    model_name: "Evaluation"
                                }
                            }
                        }
                    },
                    executionMetadata: {
                        tags: {
                            key: "trigger",
                            value: "Grafana Alert"
                        }
                    }
                }
            )
            {
                ... on LaunchRunSuccess {
                    __typename
                }
            }
        }
    """

    requests.post(
        dagster_api_url,
        json={"query": graphql_query},
        headers={"Content-Type": "application/json"},
    )

    return
