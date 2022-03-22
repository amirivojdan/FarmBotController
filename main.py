import logging
from FarmBot import FarmBot
from tkinter import *
from tkinter import ttk

from FarmBotGUI import FarmBotGUI

logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    farmbot = FarmBot()
    farmbot.connect()
    farmbot.start()

    FarmBotGUI(farmbot)

    logging.debug("Well Done!")
