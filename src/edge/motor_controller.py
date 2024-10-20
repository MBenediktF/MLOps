import os
import RPi.GPIO as GPIO
import time

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


def set_pwm_output(channel, period, duty_cycle):
    channel = str(channel)
    if channel not in ["0", "1"]:
        raise ValueError("Channel 0 and 1 supported, unknown channel")
    if not os.path.exists(f"/sys/class/pwm/pwmchip0/pwm{channel}"):
        write_pwm_config("export", channel)
        time.sleep(0.01)
    write_pwm_config(f"pwm{channel}/period", str(period))
    write_pwm_config(f"pwm{channel}/duty_cycle", str(duty_cycle))


def enable_pwm_output(channel):
    channel = str(channel)
    if channel not in ["0", "1"]:
        raise ValueError("Channel 0 and 1 supported, unknown channel")
    write_pwm_config(f"pwm{channel}/enable", "1")


def disable_pwm_output(channel):
    channel = str(channel)
    if channel not in ["0", "1"]:
        raise ValueError("Channel 0 and 1 supported, unknown channel")
    write_pwm_config(f"pwm{channel}/enable", "0")


def main():
    set_pwm_output(0, 50000000, 40000000)
    set_pwm_output(1, 50000000, 40000000)
    enable_pwm_output(0)
    enable_pwm_output(1)
    time.sleep(5)
    disable_pwm_output(0)
    disable_pwm_output(1)
    return


if __name__ == "__main__":
    main()
