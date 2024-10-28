from log_message import log_message, ERROR
from log_features_prediction import log_features_prediction
from load_model import load_registered_model
import threading
import numpy as np
import cv2


class InferencePipeline():
    def __init__(self, model_name, model_version, measurement) -> None:
        self.model_name = model_name
        self.model_version = model_version
        self.measurement = measurement

        # load model
        try:
            self.model = load_registered_model(model_name, model_version)
        except Exception as e:
            log_message(f"Error loading model: {str(e)}", ERROR)
            self.model = None
            return
        self.image_width = self.model.input_shape[2]
        self.image_height = self.model.input_shape[1]
        log_message(f"Model loaded: {model_name} - {model_version}")

      
    def run(self, image_file, sensor_value: int = 0) -> int:
        # 0: Check if model is available
        if not self.model:
            return None

        # 1: Get and check input image
        try:
            image_data = image_file.read()
            image = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        except Exception as e:
            log_message(f"Error reading image: {str(e)}", ERROR)
            return None

        # 2: Preprocess and normalize image
        image = cv2.resize(image, (self.image_width, self.image_height))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # 3: Predict and transform
        try:
            prediction = self.model.predict(image)
            prediction_mm = int(prediction[0][0] * 250)
        except Exception as e:
            log_message(f"Error predicting image: {str(e)}", ERROR)
            return None

        # 4: Start log data thread
        log_thread = threading.Thread(
            target=log_features_prediction,
            args=(
                image_data,
                prediction_mm,
                sensor_value,
                self.measurement,
                self.model_name,
                self.model_version
                )
        )
        log_thread.start()

        # 5: Return prediction
        return prediction_mm
