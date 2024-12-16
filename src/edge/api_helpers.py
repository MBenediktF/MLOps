import requests
import threading

api_url = "http://192.168.178.147:5001/predict"
client_uid = "13ff9425-ed7a-419f-a62d-c84eb7f79897"
auth_token = "ddb29c94-99a8-47a6-b924-d6bc8687caf4"


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
