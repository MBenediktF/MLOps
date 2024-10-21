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


class PWM:
    def __init__(self, channel: int) -> None:
        """
        Configures the PWM output.
        Args:
            channel (int): Selected PWM output channel [0, 1]
        """
        self.channel = str(channel)
        if self.channel not in ["0", "1"]:
            raise ValueError("Channel 0 and 1 supported, unknown channel")

    def __write(self, fname, value):
        if not os.path.exists(f"/sys/class/pwm/pwmchip0/pwm{self.channel}"):
            self.__write("export", self.channel)
            time.sleep(0.01)
        fpath = f"/sys/class/pwm/pwmchip0/{fname}"
        try:
            with open(fpath, 'w') as f:
                f.write(value)
        except IOError as e:
            print(f"Error writing to {fpath}: {e}")
            return -1
        return 0

    def set(self, period: int, duty_cycle: int) -> None:
        """
        Sets PWM period and duty cycle.
        Args:
            period (int): Period of the pwm signal in ns
            duty_cycle (int): Duty cycle of the pwm signal in ns
        """
        self.__write(f"pwm{self.channel}/period", str(period))
        self.__write(f"pwm{self.channel}/duty_cycle", str(duty_cycle))

    def enable(self) -> None:
        """
        Enables the PWM output.
        """
        self.__write(f"pwm{self.channel}/enable", "1")

    def disable(self) -> None:
        """
        Disables the PWM output.
        """
        self.__write(f"pwm{self.channel}/enable", "0")


def main():
    pwm0 = PWM(0)
    pwm1 = PWM(1)
    pwm0.set(100000, 20000)
    pwm0.enable()
    time.sleep(5)
    pwm0.disable()
    time.sleep(1)
    pwm1.set(100000, 20000)
    pwm1.enable()
    time.sleep(5)
    pwm1.disable()
    return


if __name__ == "__main__":
    main()
