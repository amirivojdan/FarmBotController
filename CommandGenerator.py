class CommandGenerator:
    """Simply generates G-Codes based on the instructions' table provided by
     the manufacturer in
    https://github.com/farmbot/farmbot-arduino-firmware#codes-sent-to-the-arduino """

    def __init__(self):
        pass

    def approve(self):
        return "F22 P2 V1 Q0"

    def move(self, x, y, z):
        return "G00 X{x} Y{y} Z{z} Q0".format(x=x, y=y, z=z)

    def move_home_all(self):
        return "G28"