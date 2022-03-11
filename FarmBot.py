from CommandGenerator import CommandGenerator
from CommunicationBus import CommunicationBus
from FarmBotStatus import FarmBotStatus


class FarmBot:
    """High-level python class to wrap all underlying details required to control
    the FarmBot."""

    def __init__(self, port, baud_rate=115200, status_update_frequency=100, logging_enabled=True):

        self.status = FarmBotStatus()
        self.command_generator = CommandGenerator()
        self.serial_bus = CommunicationBus(port, baud_rate)
        self.status_update_interval = 1/status_update_frequency  # T=1/f

    def connect(self):
        self.serial_bus.connect()

    def disconnect(self):
        self.serial_bus.disconnect()

    def approve(self):
        approval_command = self.command_generator.approve()
        self.serial_bus.send(approval_command)

    def move(self, x, y, z, x_speed, y_speed, z_speed):
        command = self.command_generator.move(x, y, z, x_speed, y_speed, z_speed)
        self.serial_bus.send(command)
        self.approve()

    def update_status(self):
        raw_responses = self.serial_bus.fetch_responses()
        if raw_responses is not None:
            for item in raw_responses:
                self.status.update(item)
