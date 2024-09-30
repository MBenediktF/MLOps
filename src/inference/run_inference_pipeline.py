from .log_message import log_message, INFO, WARNING, ERROR
from .log_features_prediction import log_features_prediction
from .load_model_tensorflow import load_model_with_best_accuracy
from .send_report_email import send_report_email
import numpy as np


def run_inference_pipeline(features):
    send_report_email("Pipeline Started", "The inference pipeline has started")

    features = np.array([1, 2, 3, 4, 5])
    prediction = {
        'result': 0.8
    }

    log_message("This is a random warning", WARNING)

    try:
        model = load_model_with_best_accuracy("MNIST Single Run")
        prediction = model.predict(features)
        log_message("Prediction successful", INFO)
    except Exception as e:
        print(str(e))
        log_message(str(e), ERROR)
        prediction = None

    log_features_prediction("edge_device_1", features, prediction)
