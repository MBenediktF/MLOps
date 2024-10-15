import requests
import threading

api_url = "http://192.168.178.147:5001/predict"


def send_measurement_to_api_thread(image, sensor_value):
    files = {'image': image}
    data = {'sensor_value': sensor_value}
    response = requests.post(api_url, files=files, data=data)
    print(f"API Response: {response.status_code}, {response.text}")


def send_measurement_to_api(image, sensor_value):
    api_thread = threading.Thread(
        target=send_measurement_to_api,
        args=(image, sensor_value)
        )
    api_thread.start()
