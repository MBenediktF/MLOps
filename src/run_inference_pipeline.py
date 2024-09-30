from inference.log_message import log_message, INFO, WARNING, ERROR
from inference.log_features_prediction import log_features_prediction

import numpy as np

log_message("Hallo Welt!", INFO)
log_message("Hallo Welt!", WARNING)
log_message("Hallo Welt!", ERROR)

features = np.array([1, 2, 3, 4, 5])
prediction = {
    'result': 0.8
}

log_features_prediction("edge_device_1", features, prediction)
