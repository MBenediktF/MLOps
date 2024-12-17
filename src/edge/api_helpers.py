import requests
import threading

api_url = "http://192.168.178.147:5001/predict"
client_uid = "d1c03ea4-b770-4675-87d5-9cdd9386beb8"
auth_token = "9e9ecc6e-7154-4e65-bed2-4533fbd78926"


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
