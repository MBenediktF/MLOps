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


if __name__ == "__main__":
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
