import time
from api_helpers import send_measurement_to_api
from capture_image import capture_image_jpg
from take_lidar_measurement import take_lidar_measurement
from buzzer_output import set_beep_interval

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

    # api call
    send_measurement_to_api(image, sensor_value)
