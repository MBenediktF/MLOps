import RPi.GPIO as GPIO
import time
import atexit

GPIO.setmode(GPIO.BCM)
LED_PIN = 24
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.HIGH)

atexit.register(lambda: GPIO.cleanup(LED_PIN))


def set_led_output(state):
    if state:
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)


if __name__ == "__main__":
    while True:
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
