from api_helpers import send_measurement_to_api
from camera import capture_image_jpg
from lidar import take_lidar_measurement
from buzzer_output import set_beep_interval
from led import set_led_output
from drive_helpers import drive, enable_controller
from gamepad import event_actions
import threading
# from button_input import wait_for_button_press_release
import time


start_distance = 350

use_prediction = True

parking = threading.Event()


def stop():
    parking.clear()


def park():
    # drive to wall and take images
    parking.set()

    while parking.is_set():
        # read lidar sensor
        sensor_value = take_lidar_measurement()
        if sensor_value is None:
            print("Could not get measurement")
            break
        distance = sensor_value - 35
        print(f"Distance: {distance}")

        if distance < start_distance:
            # take image
            image = capture_image_jpg()
            if image is None:
                print("Could not capture image")
                continue

            # api call
            if use_prediction:
                prediction = send_measurement_to_api(
                    image,
                    distance,
                    use_threading=False
                )
                distance = prediction
            else:
                send_measurement_to_api(image, distance, use_threading=True)

        set_led_output(distance <= start_distance)
        set_beep_interval(distance)

        # set motor speed
        if distance <= 20:
            target_speed = 0
        elif distance <= 100:
            target_speed = 3
        elif distance <= start_distance:
            target_speed = 5
        else:
            target_speed = 15
        drive(target_speed)

        # stop if distance to small
        if target_speed == 0:
            set_beep_interval(1)
            time.sleep(1)
            break

        time.sleep(0.25)

    print("Finished.")
    target_speed = 0
    drive(target_speed)
    set_beep_interval(300)
    set_led_output(False)
    time.sleep(1)


def start_parking():
    park_thread = threading.Thread(target=park)
    park_thread.start()


enable_controller()
event_actions['x_pressed'] = start_parking
event_actions['x_released'] = stop
