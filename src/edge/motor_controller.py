import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DIR_LEFT_PIN = 6
DIR_RIGHT_PIN = 16
GPIO.setup(DIR_LEFT_PIN, GPIO.OUT)
GPIO.setup(DIR_RIGHT_PIN, GPIO.OUT)
GPIO.output(DIR_LEFT_PIN, GPIO.HIGH)
GPIO.output(DIR_RIGHT_PIN, GPIO.HIGH)


def write_pwm_config(fname, value):
    fpath = f"/sys/class/pwm/pwmchip0/{fname}"
    try:
        with open(fpath, 'w') as f:
            f.write(value)
    except IOError as e:
        print(f"Error writing to {fpath}: {e}")
        return -1
    return 0


def main():
    if not os.path.exists("/sys/class/pwm/pwmchip0/pwm0"):
        ret = write_pwm_config("export", "0")
        if ret:
            return ret

    ret = write_pwm_config("pwm0/period", "500000000")  # 500ms period (2 Hz)
    if ret:
        return ret

    ret = write_pwm_config("pwm0/duty_cycle", "400000000")  # 80% Duty Cycle
    if ret:
        return ret

    ret = write_pwm_config("pwm0/enable", "1")  # Enable PWM
    if ret:
        return ret

    if not os.path.exists("/sys/class/pwm/pwmchip0/pwm1"):
        ret = write_pwm_config("export", "1")
        if ret:
            return ret

    ret = write_pwm_config("pwm1/period", "500000000")  # 500ms period (2 Hz)
    if ret:
        return ret

    ret = write_pwm_config("pwm1/duty_cycle", "400000000")  # 80% Duty Cycle
    if ret:
        return ret

    ret = write_pwm_config("pwm1/enable", "1")  # Enable PWM
    if ret:
        return ret

    return 0


if __name__ == "__main__":
    main()
