# send measurements from json file to inference api
import json
import time
import numpy as np
import requests
import threading
import cv2


measurement = "env_beige_default"  # download from mbenediktf.de/end-to-end-mlops/simdata
send_interval = 0.2  # seconds
max_send = 1000  # maximum number of measurements to send
api_url = "http://localhost:5001/predict"
client_uid = "d1c03ea4-b770-4675-87d5-9cdd9386beb8"  # change!
auth_token = "9e9ecc6e-7154-4e65-bed2-4533fbd78926"  # change!


def send_measurement_to_api_thread(image, sensor_value):
    files = {'image': image}
    data = {
        'sensor_value': sensor_value,
        'client_uid': client_uid
        }
    headers = {
        'Authorization': auth_token
        }
    response = requests.post(api_url, files=files, headers=headers, data=data)
    if response.status_code != 200:
        print(f"API Response: {response.status_code}, {response.text}")


def send_measurement_to_api(image, sensor_value):
    api_thread = threading.Thread(
        target=send_measurement_to_api_thread,
        args=(image, sensor_value)
        )
    api_thread.start()


print("Importing data...")

# get dataset from json file
with open(f"src/scripts/simdata/{measurement}.json", "r") as file:
    input_data = json.load(file)
images = np.array(input_data["images"], dtype=np.uint8)
labels = np.array(input_data["labels"], dtype=np.uint16)
uids = np.array(input_data["uids"])

print(f"Dataset imported: {len(images)} images")
print("Sending measurements...")

# send measurements to api
max_send = min(max_send, len(images))
for i in range(max_send):
    print(f"Sending image {i+1}/{max_send}")
    _, encoded_image = cv2.imencode('.jpg', images[i])
    image_file = ("image.jpg", encoded_image, 'image/jpeg')
    send_measurement_to_api(image_file, labels[i])
    time.sleep(send_interval)

print("Finished.")
