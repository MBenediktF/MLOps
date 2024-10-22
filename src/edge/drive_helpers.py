from wheel import wheel_left, wheel_right

DRIVE_SPEED = 35
ROTATE_SPEED = 30
MAX_SPEED = 60
LEFT_WHEEL_CORRECTION = 2

speed = DRIVE_SPEED
wheel_left_speed = 0
wheel_right_speed = 0


def __set_speed():
    wheel_left.set_speed(wheel_left_speed)
    wheel_right.set_speed(wheel_right_speed)


def rotate_right():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = (ROTATE_SPEED + LEFT_WHEEL_CORRECTION) * -1
    wheel_right_speed = ROTATE_SPEED
    __set_speed()


def rotate_left():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = ROTATE_SPEED + LEFT_WHEEL_CORRECTION
    wheel_right_speed = ROTATE_SPEED * -1
    __set_speed()


def drive_forward():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = DRIVE_SPEED + LEFT_WHEEL_CORRECTION
    wheel_right_speed = DRIVE_SPEED
    __set_speed()


def drive_backward():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = (DRIVE_SPEED + LEFT_WHEEL_CORRECTION) * -1
    wheel_right_speed = DRIVE_SPEED * -1
    __set_speed()


def enable_speed_mode():
    global wheel_right_speed
    global wheel_left_speed
    if wheel_right_speed == DRIVE_SPEED:
        wheel_left_speed = MAX_SPEED + LEFT_WHEEL_CORRECTION
        wheel_right_speed = MAX_SPEED
    elif wheel_right_speed == DRIVE_SPEED * -1:
        wheel_left_speed = (MAX_SPEED + LEFT_WHEEL_CORRECTION) * -1
        wheel_right_speed = MAX_SPEED * -1
    else:
        return
    __set_speed()


def disable_speed_mode():
    global wheel_right_speed
    global wheel_left_speed
    if wheel_right_speed == MAX_SPEED:
        wheel_left_speed = DRIVE_SPEED + LEFT_WHEEL_CORRECTION
        wheel_right_speed = DRIVE_SPEED
    elif wheel_right_speed == MAX_SPEED * -1:
        wheel_left_speed = (DRIVE_SPEED + LEFT_WHEEL_CORRECTION) * -1
        wheel_right_speed = DRIVE_SPEED * -1
    else:
        return
    __set_speed()


def drive(speed):
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = speed + LEFT_WHEEL_CORRECTION
    wheel_right_speed = speed
    __set_speed()


def drive_stop():
    global wheel_right_speed
    global wheel_left_speed
    wheel_left_speed = 0
    wheel_right_speed = 0
    __set_speed()
