from evdev import InputDevice
from threading import Thread

gamepad = InputDevice('/dev/input/event4')

# Event-Callback-Definitionen
event_actions = {
    'up': lambda: print("Up pressed"),
    'down': lambda: print("Down pressed"),
    'left': lambda: print("Left pressed"),
    'right': lambda: print("Right pressed"),
    'released': lambda: print("Released"),
    'x_pressed': lambda: print("X pressed"),
    'x_released': lambda: print("X released"),
    'r2_pressed': lambda: print("R2 pressed"),
    'r2_released': lambda: print("R2 released")
}


def handle_event(event_code, event_value):
    if event_code == 17 and event_value == -1:
        event_actions['up']()
    elif event_code == 17 and event_value == 1:
        event_actions['down']()
    elif event_code == 16 and event_value == -1:
        event_actions['left']()
    elif event_code == 16 and event_value == 1:
        event_actions['right']()
    elif event_code in [16, 17] and event_value == 0:
        event_actions['released']()
    elif event_code == 304 and event_value == 1:
        event_actions['x_pressed']()
    elif event_code == 304 and event_value == 0:
        event_actions['x_released']()
    elif event_code == 313 and event_value == 1:
        event_actions['r2_pressed']()
    elif event_code == 313 and event_value == 0:
        event_actions['r2_released']()


def run_event_loop():
    for event in gamepad.read_loop():
        handle_event(event.code, event.value)


event_loop_thread = Thread(target=run_event_loop)
event_loop_thread.start()
