import libcamera
from picamera2 import Picamera2
import cv2
import atexit

picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (2592, 1944)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picam.configure(config)
picam.start()

atexit.register(picam.close)


def capture_image_jpg():
    try:
        image = picam.capture_array()
        image = cv2.resize(image, (640, 480))
        _, encoded_image = cv2.imencode('.jpg', image)
        file = ('image.jpg', encoded_image.tobytes(), 'image/jpeg')
        return file
    except Exception:
        return False
