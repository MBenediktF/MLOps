from evdev import InputDevice

gamepad = InputDevice('/dev/input/event4')

for event in gamepad.read_loop():
    # print(f"{event.code}, {event.value}")
    if event.code == 17 and event.value == -1:
        print("Up pressed")
    elif event.code == 17 and event.value == 1:
        print("Down pressed")
    elif event.code == 16 and event.value == -1:
        print("Left pressed")
    elif event.code == 16 and event.value == 1:
        print("Right pressed")
    elif event.code in [16, 17] and event.value == 0:
        print("Released")
    elif event.code == 304 and event.value == 1:
        print("X pressed")
    elif event.code == 304 and event.value == 0:
        print("X released")
    elif event.code == 313 and event.value == 1:
        print("R2 pressed")
    elif event.code == 313 and event.value == 0:
        print("R2 released")
