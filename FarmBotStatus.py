class FarmBotStatus:
    """Receives the packets from the FarmBot and interpret them according to
     the table provided by the manufacturer in
     https://github.com/farmbot/farmbot-arduino-firmware#codes-received-from-the-arduino """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def update(self, raw_response):
        pass
