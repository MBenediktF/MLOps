from api_helpers import send_measurement_to_api
from camera import capture_image_jpg
from edge.lidar import take_lidar_measurement
from buzzer_output import set_beep_interval
from edge.led import set_led_output
from drive_helpers import drive, enable_controller
from edge.gamepad import event_actions
# from button_input import wait_for_button_press_release
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

        set_led_output(distance <= 250)
        set_beep_interval(distance)

        # set motor speed
        if distance <= 12:
            target_speed = 0
        elif distance <= 100:
            target_speed = 3
        elif distance <= 250:
            target_speed = 5
        else:
            target_speed = 15
        drive(target_speed)

        if distance < 250:
            # take image
            image = capture_image_jpg()
            if image is None:
                print("Could not capture image")
                continue

            # api call
            send_measurement_to_api(image, sensor_value)

        # stop if distance to small
        if target_speed == 0:
            set_beep_interval(1)
            time.sleep(1)
            set_beep_interval(300)
            set_led_output(False)
            break

        time.sleep(0.25)

    print("Finished.")
    time.sleep(1)


enable_controller()
event_actions['x_pressed'] = park
