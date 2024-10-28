import requests
import threading

api_url = "http://192.168.178.147:5001/predict"
client_uid = "c04bc4d0-f6c0-4166-ae1a-c25b64e14044"
auth_token = "b77d9a12-1f98-4297-8c6e-01f3758ead85"


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
    print(f"API Response: {response.status_code}, {response.text}")


def send_measurement_to_api(image, sensor_value):
    api_thread = threading.Thread(
        target=send_measurement_to_api_thread,
        args=(image, sensor_value)
        )
    api_thread.start()
