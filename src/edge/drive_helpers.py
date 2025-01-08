from wheel import wheel_left, wheel_right
from gamepad import event_actions

DRIVE_SPEED = 25
ROTATE_SPEED = 15
MAX_SPEED = 40

speed = DRIVE_SPEED
wheel_left_speed = 0
wheel_right_speed = 0


def __set_speed():
    wheel_left.set_speed(wheel_left_speed)
    wheel_right.set_speed(wheel_right_speed)


def __rotate_right():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = ROTATE_SPEED * -1
    wheel_right_speed = ROTATE_SPEED
    __set_speed()


def __rotate_left():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = ROTATE_SPEED
    wheel_right_speed = ROTATE_SPEED * -1
    __set_speed()


def __drive_forward():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = DRIVE_SPEED
    wheel_right_speed = DRIVE_SPEED
    __set_speed()


def __drive_backward():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = DRIVE_SPEED * -1
    wheel_right_speed = DRIVE_SPEED * -1
    __set_speed()


def __enable_speed_mode():
    global wheel_right_speed
    global wheel_left_speed
    if wheel_right_speed == DRIVE_SPEED:
        wheel_left_speed = MAX_SPEED
        wheel_right_speed = MAX_SPEED
    elif wheel_right_speed == DRIVE_SPEED * -1:
        wheel_left_speed = MAX_SPEED * -1
        wheel_right_speed = MAX_SPEED * -1
    else:
        return
    __set_speed()


def __disable_speed_mode():
    global wheel_right_speed
    global wheel_left_speed
    if wheel_right_speed == MAX_SPEED:
        wheel_left_speed = DRIVE_SPEED
        wheel_right_speed = DRIVE_SPEED
    elif wheel_right_speed == MAX_SPEED * -1:
        wheel_left_speed = DRIVE_SPEED * -1
        wheel_right_speed = DRIVE_SPEED * -1
    else:
        return
    __set_speed()


def __drive_stop():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = 0
    wheel_right_speed = 0
    __set_speed()


def drive(speed):
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = speed
    wheel_right_speed = speed
    __set_speed()


def enable_controller():
    event_actions['up'] = __drive_forward
    event_actions['down'] = __drive_backward
    event_actions['left'] = __rotate_left
    event_actions['right'] = __rotate_right
    event_actions['released'] = __drive_stop
    event_actions['r2_pressed'] = __enable_speed_mode
    event_actions['r2_released'] = __disable_speed_mode


if __name__ == "__main__":
    enable_controller()
