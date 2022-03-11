class CommandGenerator:
    """Simply generates G-Codes based on the instructions' table provided by
     the manufacturer in
    https://github.com/farmbot/farmbot-arduino-firmware#codes-sent-to-the-arduino """

    def __init__(self):
        pass

    def approve(self):
        return 'F22 P2 V1 Q0'

    def move(self, x, y, z, x_speed, y_speed, z_speed):
        return 'G00 X{x} Y{y} Z{z} A{x_speed} B{y_speed} C{z_speed} Q0'.format(x=x, y=y, z=z,
                                                                               x_speed=x_speed,
                                                                               y_speed=y_speed,
                                                                               z_speed=z_speed)

    def move_home_all(self):
        return 'G28'
