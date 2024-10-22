import time
import RPi.GPIO as GPIO
import atexit

WHEEL_LEFT_INTERRUPT_PIN = 26
WHEEL_RIGHT_INTERRUPT_PIN = 19

atexit.register(lambda: GPIO.cleanup(WHEEL_LEFT_INTERRUPT_PIN))
atexit.register(lambda: GPIO.cleanup(WHEEL_RIGHT_INTERRUPT_PIN))

n_left = 0
n_right = 0


def wheel_left_callback(_):
    global n_left
    n_left += 1


def wheel_right_callback(_):
    global n_right
    n_right += 1


def get_rotation_count():
    global n_left, n_right
    return n_left, n_right


def reset_rotation_count():
    global n_left, n_right
    n_left, n_right = 0, 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(
    WHEEL_LEFT_INTERRUPT_PIN,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP)
GPIO.setup(
    WHEEL_RIGHT_INTERRUPT_PIN,
    GPIO.IN,
    pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(
    WHEEL_LEFT_INTERRUPT_PIN,
    GPIO.FALLING,
    callback=wheel_left_callback,
    bouncetime=1)
GPIO.add_event_detect(
    WHEEL_RIGHT_INTERRUPT_PIN,
    GPIO.FALLING,
    callback=wheel_right_callback,
    bouncetime=1)


if __name__ == '__main__':
    while True:
        left, right = get_rotation_count()
        reset_rotation_count()
        print(f"l: {left}, r: {right}")
        time.sleep(1)
