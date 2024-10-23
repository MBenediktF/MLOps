from picamera2 import Picamera2
import cv2
import atexit

picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (4608, 2592)})
picam.configure(config)
picam.start()

atexit.register(picam.close)


def capture_image_jpg():
    try:
        # capture and convert image
        image = picam.capture_array()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # crop image to 4:3
        image = image[:, 567:4032]

        # reduce image resolution
        image = cv2.resize(image, (640, 480))

        # encode image
        _, encoded_image = cv2.imencode('.jpg', image)
        file = ('image.jpg', encoded_image.tobytes(), 'image/jpeg')
        return file
    except Exception:
        return False
