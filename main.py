from time import sleep

from Extreme3dPro import Extreme3dPro
from FarmBot import FarmBot

if __name__ == '__main__':
    # farmbot = FarmBot("COM5")
    # farmbot.connect()
    # farmbot.start()
    controller = Extreme3dPro()
    while True:
        controller.update()
        print("pitch:{pitch}  roll:{roll}  yaw:{yaw}".format(pitch=controller.pitch,
                                                             roll=controller.roll,
                                                             yaw=controller.yaw))
        i = 0
        for btn in controller.buttons_status:
            print("{btn_i} : {btn}".format(btn_i=i, btn=btn))
            i += 1
        sleep(0.01)
    print("Well Done!")
