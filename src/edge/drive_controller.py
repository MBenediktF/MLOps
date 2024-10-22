from wheel import wheel_left, wheel_right
from interrupts import get_rotation_count
import time
import atexit

atexit.register(lambda: wheel_left.set_speed(0))
atexit.register(lambda: wheel_right.set_speed(0))

K_p = 0.5
target_speed = 50

while True:
    n_left, n_right = get_rotation_count()
    diff = abs(n_left-n_right)
    print(diff)

    target_speed_left, target_speed_right = target_speed, target_speed
    if n_left < n_right:
        target_speed_left += K_p * diff
    else:
        target_speed_right += K_p * diff

    target_speed_left = max(0, min(100, target_speed_left))
    target_speed_right = max(0, min(100, target_speed_right))

    print(f"New target speed: l: {target_speed_left}, r: {target_speed_right}")

    wheel_left.set_speed(target_speed_left)
    wheel_right.set_speed(target_speed_right)

    time.sleep(0.1)
