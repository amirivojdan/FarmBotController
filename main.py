from time import sleep

import CommandGenerator
import Communication
from pynput import keyboard


def on_press(key):
    try:
        if key.char == "a":
            print("Left")
        if key.char == "d":
            print("Right")
        if key.char == "w":
            print("Forward")
        if key.char == "s":
            print("Backward")
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


if __name__ == '__main__':
    command_bus = Communication.Communication("COM5")
    print("Connected!")

    command_generator = CommandGenerator.CommandGenerator()
    while True:

        sleep(0.01)
        if command_bus.serial.inWaiting():
            line = command_bus.serial.readline()
            line = line.decode('ascii')
            print(line)
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("Well Done!")
