import libcamera
from picamera2 import Picamera2
import time
import requests
import cv2

picam = Picamera2()
config = picam.create_preview_configuration(main={"size": (640, 480)})
config["transform"] = libcamera.Transform(hflip=0, vflip=1)
picam.configure(config)
picam.start()

api_url = "http://192.168.178.133:5001/upload"

while True:
	image = picam.capture_array()
	_, encoded_image = cv2.imencode('.jpg', image)
	files = {'image': ('image.jpg', encoded_image.tobytes(), 'image/jpeg')}
	response = requests.post(api_url, files=files)
	print(f"API Response: {response.status_code}, {response.text}")
	time.sleep(1)
	
picam.close()
