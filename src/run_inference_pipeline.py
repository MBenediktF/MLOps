from inference.log_message import log_message, INFO, WARNING, ERROR
from inference.log_features_prediction import log_features_prediction
from inference.load_model_tensorflow import load_model_with_best_accuracy

import numpy as np

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
