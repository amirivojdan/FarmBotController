from time import sleep
from FarmBot import FarmBot

if __name__ == '__main__':
    farmbot = FarmBot("COM8")
    farmbot.connect()
    farmbot.start()
    print("Well Done!")
