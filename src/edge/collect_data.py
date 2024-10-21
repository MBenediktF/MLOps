from api_helpers import send_measurement_to_api
from capture_image import capture_image_jpg
from take_lidar_measurement import take_lidar_measurement
from buzzer_output import set_beep_interval
from led_output import set_led_output
from drive import drive, drive_forward, drive_backward, drive_stop
from drive import rotate_left, rotate_right
from drive import enable_speed_mode, disable_speed_mode
# from button_input import wait_for_button_press_release
from controller_input import event_actions
import time


def park():
    # drive to wall and take images
    while True:
        # read lidar sensor
        sensor_value = take_lidar_measurement()
        if sensor_value is None:
            print("Could not get measurement")
            break
        distance = sensor_value - 35
        print(f"Distance: {distance}")

        set_led_output(distance <= 200)
        set_beep_interval(distance)

        # set motor speed
        if distance <= 15:
            target_speed = 0
        elif distance <= 200:
            target_speed = 10
        else:
            target_speed = 30
        drive(target_speed)

        if distance < 200:
            # take image
            image = capture_image_jpg()
            if image is None:
                print("Could not capture image")
                continue

            # api call
            send_measurement_to_api(image, sensor_value)

        # stop if distance to small
        if target_speed == 0:
            set_beep_interval(0)
            set_led_output(False)
            break

        time.sleep(0.25)

    print("Finished.")
    time.sleep(1)


event_actions['x_pressed'] = park
event_actions['up'] = drive_forward
event_actions['down'] = drive_backward
event_actions['left'] = rotate_left
event_actions['right'] = rotate_right
event_actions['released'] = drive_stop
event_actions['r2_pressed'] = enable_speed_mode
event_actions['r2_released'] = disable_speed_mode
