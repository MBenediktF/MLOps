from log_message import log_message, ERROR
from log_features_prediction import log_features_prediction
from load_model import load_registered_model
import threading
import numpy as np
import cv2

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 75

model_name = "Dev-Live"
model_version = "latest"
measurement = "m2"


def run_inference_pipeline(image_file, sensor_value=0):
    try:
        # 1: Get and check input image
        image = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # 2: Preprocess and normalize image
        image = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # 3: Load model
        model = load_registered_model(model_name, model_version)

        # 4: Predict and transform
        prediction = model.predict(image)
        prediction_mm = int(prediction[0][0] * 250)

        # 5: Log data (thread)
        threading.Thread(
            target=log_features_prediction,
            args=(image_file, prediction_mm, sensor_value, measurement)
        ).start()

        # 6: Return prediction
        return prediction_mm

    except Exception as e:
        log_message(str(e), ERROR)
        return None
