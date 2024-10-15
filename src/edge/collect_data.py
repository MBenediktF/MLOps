import requests
import time
from capture_image import capture_image_jpg
from take_lidar_measurement import take_lidar_measurement

api_url = "http://192.168.178.133:5001/upload"


while True:
    time.sleep(0.25)

    # take image
    image = capture_image_jpg()
    if image is None:
        print("Could not capture image")
        continue

    # read lidar sensor
    measurement = take_lidar_measurement()
    if measurement is None:
        print("Could not get measurement")
        continue
    if measurement > 250:
        print("Measurement out of range")
        continue

    # send api request
    files = {'image': image}
    data = {'measurement': measurement}
    response = requests.post(api_url, files=files, data=data)
    print(f"API Response: {response.status_code}, {response.text}")
