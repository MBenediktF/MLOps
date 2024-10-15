import requests
import time
from capture_image import capture_image_jpg
from take_lidar_measurement import take_lidar_measurement
from buzzer_output import set_beep_interval

api_url = "http://192.168.178.147:5001/predict"


while True:
    time.sleep(0.25)

    # take image
    image = capture_image_jpg()
    if image is None:
        print("Could not capture image")
        continue

    # read lidar sensor
    sensor_value = take_lidar_measurement()
    if sensor_value is None:
        print("Could not get measurement")
        continue
    set_beep_interval(sensor_value-30)
    if sensor_value > 250:
        print("Measurement out of range")
        continue

    # send api request
    files = {'image': image}
    data = {'sensor_value': sensor_value}
    response = requests.post(api_url, files=files, data=data)
    print(f"API Response: {response.status_code}, {response.text}")
