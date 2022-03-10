from time import sleep

from FarmBot import FarmBot


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
    farmbot = FarmBot("COM8")
    farmbot.connect()
    print("Connected!")
    while True:
        sleep(0.01)
        farmbot.update_status()
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    print("Well Done!")
