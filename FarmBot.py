from CommandGenerator import CommandGenerator
from CommunicationBus import CommunicationBus
from FarmBotStatus import FarmBotStatus


class FarmBot:
    """High-level python class to wrap all underlying details required to control
    the FarmBot."""

    def __init__(self, port, baud_rate=115200, logging_enabled=True):
        self.status = FarmBotStatus()
        self.command_generator = CommandGenerator()
        self.serial_bus = CommunicationBus(port, baud_rate)

    def connect(self):
        self.serial_bus.connect()

    def disconnect(self):
        self.serial_bus.disconnect()

    def move(self, x, y, z):
        command = self.command_generator.move(x, y, z)
        self.serial_bus.send(command)
        approval_command = self.command_generator.approve()
        self.serial_bus.send(approval_command)

    def update_status(self):
        raw_response = self.serial_bus.fetch_response()
        if raw_response is not None:
            print(raw_response)
            self.status.update(raw_response)
