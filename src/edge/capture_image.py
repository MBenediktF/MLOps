import libcamera
from picamera2 import Picamera2
import cv2

picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (640, 480)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picam.configure(config)
picam.start()


def capture_image_jpg():
    try:
        image = picam.capture_array()
        _, encoded_image = cv2.imencode('.jpg', image)
        file = ('image.jpg', encoded_image.tobytes(), 'image/jpeg')
        return file
    except Exception:
        return False
