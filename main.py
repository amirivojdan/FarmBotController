from time import sleep
from FarmBot import FarmBot

if __name__ == '__main__':

    farmbot = FarmBot("COM8")
    farmbot.connect()
    print("Connected!")
    print("Initializing...")
    while not farmbot.status.is_initialized:
        farmbot.update_status()
        sleep(farmbot.status_update_interval)
    print("Initializing Finished!")
    farmbot.approve()
    print("Config Approved!")
    while True:
        farmbot.update_status()
        farmbot.move(1010, 1010, -201, 100, 100, 100)
    print("Well Done!")