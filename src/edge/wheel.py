import RPi.GPIO as GPIO
from pwm import PWM
import time
import atexit
import threading

DIR_LEFT_PIN = 6
DIR_RIGHT_PIN = 16
INT_LEFT_PIN = 26
INT_RIGHT_PIN = 19
K_p = 0.4
K_i = 0.027
K_d = 0.02


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
        self.speed = 0
        self.direction = 0
        self.pid_integral = 0
        self.pid_prev_diff = 0
        self.pid_steps = 0
        self.active = True

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

        atexit.register(self.cleanup)

        self.controller_thread = threading.Thread(
            target=self.__controller_thread
        )
        self.controller_thread.start()

    def __int_callback(self, _) -> None:
        self.int_count += 1

    def __controller_thread(self) -> None:
        while self.active:
            # get steps and calc diff
            steps_real = self.__get_int_count()
            steps_goal = self.pid_steps + self.speed
            self.pid_steps = steps_goal
            diff = steps_goal - steps_real

            # calc target speed (PID-controller)
            self.pid_integral += diff
            P_out = K_p * diff
            I_out = K_i * self.pid_integral
            D_out = K_d * (diff - self.pid_prev_diff)
            target_speed = P_out + I_out + D_out
            target_speed = max(0, min(100, target_speed))
            self.pid_prev_diff = diff

            # set target speed, respect direction
            if self.direction < 0:
                target_speed = target_speed * -1
            self.__set_speed_pwm(target_speed)

            time.sleep(0.1)

    def cleanup(self) -> None:
        """
        Stops all shtrads and clears GPIOs
        """
        self.speed = 0
        self.active = False
        self.int_count = 0
        self.__set_speed_pwm(0)
        GPIO.cleanup(self.dir_pin)
        GPIO.cleanup(self.int_pin)

    def __get_int_count(self) -> int:
        """
        Returns wheel interrupt count
        Return:
            count (int): Interrupt count
        """
        return self.int_count

    def __set_speed_pwm(self, speed: int) -> None:
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
            raise ValueError("Speed has to be an integer -100 to 100")

    def set_speed(self, speed: int) -> None:
        self.speed = abs(speed)
        if speed < 0:
            self.direction = -1
        elif speed > 0:
            self.direction = +1


wheel_left = WHEEL(0, DIR_LEFT_PIN, INT_LEFT_PIN)
wheel_right = WHEEL(1, DIR_RIGHT_PIN, INT_RIGHT_PIN)


def main():
    wheel_left.set_speed(10)
    wheel_right.set_speed(10)
    time.sleep(3)
    wheel_left.set_speed(0)
    wheel_right.set_speed(0)
    time.sleep(1)
    wheel_left.set_speed(-10)
    wheel_right.set_speed(-10)
    time.sleep(3)
    wheel_left.set_speed(0)
    wheel_right.set_speed(0)
    wheel_left.cleanup()
    wheel_right.cleanup()


if __name__ == "__main__":
    main()
