import RPi.GPIO as GPIO
import time
import threading
from take_lidar_measurement import take_lidar_measurement
import atexit

BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, 600)
buzzer.start(0)

beep_interval = 1.5

atexit.register(lambda: GPIO.cleanup(BUZZER_PIN))


def buzzer_thread():
    global beep_interval
    while True:
        if beep_interval > 1:
            continue
        buzzer.ChangeDutyCycle(50)
        time.sleep(0.03)
        if beep_interval <= 0:
            continue
        buzzer.ChangeDutyCycle(0)
        time.sleep(beep_interval)


buzzer_control_thread = threading.Thread(target=buzzer_thread)
buzzer_control_thread.start()


def set_beep_interval(distance):
    global beep_interval
    if distance > 200:
        beep_interval = 1.5
    elif 100 < distance <= 200:
        beep_interval = 0.8
    elif 70 < distance <= 120:
        beep_interval = 0.5
    elif 30 < distance <= 70:
        beep_interval = 0.3
    elif 10 < distance <= 30:
        beep_interval = 0.12
    else:
        beep_interval = 0


if __name__ == "__main__":
    while True:
        time.sleep(0.25)
        sensor_value = take_lidar_measurement()-30
        if sensor_value is None:
            print("Could not get measurement")
            continue
        set_beep_interval(sensor_value)
