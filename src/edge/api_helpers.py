import requests
import threading
import json

api_url = "http://192.168.178.147:5001/predict"
client_uid = "35accd53-aa1b-4809-b929-0fda258401ab"
auth_token = "5bbe8d9c-3a42-4536-9c6a-aed52fd1a745"


def __send_measurement_to_api(image, sensor_value):
    files = {'image': image}
    data = {
        'sensor_value': sensor_value,
        'client_uid': client_uid
        }
    headers = {
        'Authorization': auth_token
        }
    response = requests.post(api_url, files=files, headers=headers, data=data)
    print(f"API Response: {response.status_code}, {response.text}")
    try:
        response_dict = json.loads(response.text)
        return int(response_dict["prediction"])
    except Exception:
        return


def send_measurement_to_api(image, sensor_value, use_threading=False):
    if use_threading:
        api_thread = threading.Thread(
            target=__send_measurement_to_api,
            args=(image, sensor_value)
            )
        api_thread.start()
    else:
        return __send_measurement_to_api(image, sensor_value)
