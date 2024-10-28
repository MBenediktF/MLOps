import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

BUTTON_PIN = 14
GPIO.setup(BUTTON_PIN, GPIO.IN)


def get_button_pressed_state():
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        return False
    else:
        return True


def wait_for_button_press_release():
    while not get_button_pressed_state():
        pass
    time.sleep(0.1)
    while get_button_pressed_state():
        pass
    time.sleep(0.1)


if __name__ == "__main__":
    print("Waiting for button press release")
    wait_for_button_press_release()
    print("Checking for Button presses")
    while True:
        while not get_button_pressed_state():
            continue
        print("Button pressed")
        time.sleep(0.01)
        while get_button_pressed_state():
            continue
        print("Button released")
        time.sleep(0.01)
