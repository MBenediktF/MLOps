import RPi.GPIO as GPIO
from pwm import PWM
import time
import atexit

DIR_LEFT_PIN = 6
DIR_RIGHT_PIN = 16
INT_LEFT_PIN = 26
INT_RIGHT_PIN = 19


class WHEEL:
    def __init__(self, pwm_channel: int, dir_pin: int, int_pin: int) -> None:
        """
        Configures a wheel.
        Args:
            pwm_channel (int): Selected PWM output channel [0, 1]
            dir_pin (int): Motor direction pin
        """
        self.pwm = PWM(pwm_channel)
        self.dir_pin = dir_pin
        self.int_pin = int_pin
        self.int_count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir_pin, GPIO.OUT)

        GPIO.setup(
            self.int_pin,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            self.int_pin,
            GPIO.FALLING,
            callback=self.__int_callback,
            bouncetime=1)

        atexit.register(lambda: GPIO.cleanup(self.dir_pin))
        atexit.register(lambda: GPIO.cleanup(self.int_pin))
        self.set_speed(0)

    def __int_callback(self, _) -> None:
        self.int_count += 1

    def get_int_count(self) -> int:
        """
        Returns wheel interrupt count
        Return:
            count (int): Interrupt count
        """
        return self.int_count

    def reset_int_count(self) -> None:
        self.int_count = 0

    def set_speed(self, speed: float) -> None:
        """
        Sets wheel speed and direction.
        Args:
            speed (int): Target speed [-100:100]
        """
        if speed == 0:
            self.pwm.disable()
            return

        if speed < 0:
            GPIO.output(self.dir_pin, GPIO.LOW)
        else:
            GPIO.output(self.dir_pin, GPIO.HIGH)

        if abs(speed) <= 100:
            self.pwm.set(100000, int(100000/200*abs(speed)))
            self.pwm.enable()
        else:
            raise ValueError("Speed has to be an integer from 0 to 100")


wheel_left = WHEEL(0, DIR_LEFT_PIN, INT_LEFT_PIN)
wheel_right = WHEEL(1, DIR_RIGHT_PIN, INT_RIGHT_PIN)


def main():
    wheel_left.set_speed(50)
    wheel_right.set_speed(50)
    time.sleep(5)
    wheel_left.set_speed(0)
    wheel_right.set_speed(0)
    time.sleep(1)
    wheel_left.set_speed(-50)
    wheel_right.set_speed(-50)
    time.sleep(5)
    wheel_left.set_speed(0)
    wheel_right.set_speed(0)
    return


if __name__ == "__main__":
    main()
