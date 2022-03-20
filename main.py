import logging
from FarmBot import FarmBot
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    farmbot = FarmBot("COM8")
    farmbot.connect()
    farmbot.start()

    logging.debug("Well Done!")
