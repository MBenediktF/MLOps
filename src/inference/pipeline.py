from helpers.logs import Log, ERROR
from log_run import log_run
from load_model import load_registered_model
from tables.deployments import get_active_deployment
import threading
import numpy as np
import cv2

log = Log()

max_input_value = 350


class InferencePipeline():
    def __init__(self) -> None:
        # get deployment
        self.measurement = ""
        self.model_name = ""
        self.model_version = ""
        self.model = None
        self.setup_deployment()
        # placeholders, will be overwritten by model
        self.image_width = 100
        self.image_height = 75

    def setup_deployment(self):
        active_deployment = get_active_deployment()

        if active_deployment[0] == self.measurement:
            return

        log.log(f"New active deployment: {active_deployment}")
        self.measurement = active_deployment[0]
        self.model_name = active_deployment[1]
        self.model_version = active_deployment[2]
        if (
            not self.measurement or
            not self.model_name or
            not self.model_version
        ):
            log.log("No active deployment found", ERROR)
            self.model = None
            return

        # load model
        try:
            self.model = load_registered_model(
                self.model_name,
                self.model_version
                )
        except Exception as e:
            log.log(f"Error loading model: {str(e)}", ERROR)
            self.model = None
            return
        self.image_width = self.model.input_shape[2]
        self.image_height = self.model.input_shape[1]
        log.log(f"Model loaded: {self.model_name} - {self.model_version}")

    def run(self, client_uid: str, image_file, sensor_value: int = 0) -> int:
        self.setup_deployment()

        # 1: Get and check input image
        try:
            image_data = image_file.read()
            image = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        except Exception as e:
            log.log(f"Error reading image: {str(e)}", ERROR)
            return None

        # 2: Preprocess and normalize image
        image = cv2.resize(image, (self.image_width, self.image_height))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)

        # 3: Predict and transform if there's a model
        if self.model:
            try:
                prediction = self.model.predict(image)
                prediction_mm = int(prediction[0][0] * max_input_value)
            except Exception as e:
                log.log(f"Error predicting image: {str(e)}", ERROR)
                return None
        else:
            prediction_mm = None

        # 4: Start log data thread
        log_thread = threading.Thread(
            target=log_run,
            args=(
                client_uid,
                image_data,
                prediction_mm,
                sensor_value,
                self.measurement,
                self.model_name,
                self.model_version,
                )
        )
        log_thread.start()

        # 5: Return prediction
        return prediction_mm
