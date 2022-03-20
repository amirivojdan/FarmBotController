from threading import Thread
from time import sleep
from CommandGenerator import CommandGenerator
from CommunicationBus import CommunicationBus
from FarmBotStatus import FarmBotStatus
import logging


class FarmBot(Thread):
    """High-level python class to wrap all underlying details required to control
    the FarmBot."""

    def __init__(self, port, baud_rate=115200, command_update_frequency=200,
                 status_update_frequency=200, logging_enabled=True):
        Thread.__init__(self)
        self.done = False
        self.serial_bus = CommunicationBus(port, baud_rate)
        self.status = FarmBotStatus(status_update_frequency, self.serial_bus)
        self.command_generator = CommandGenerator()
        self.command_update_interval = 1/command_update_frequency  # T=1/f

    def connect(self):
        logging.debug("Connected!")
        self.serial_bus.connect()

    def disconnect(self):
        logging.debug("Disconnected!")
        self.serial_bus.disconnect()

    def approve(self):
        approval_command = self.command_generator.approve()
        self.serial_bus.send(approval_command)

    def move(self, x, y, z, x_speed, y_speed, z_speed):
        command = self.command_generator.move(x, y, z, x_speed, y_speed, z_speed)
        self.serial_bus.send(command)
        self.approve()

    def run(self):
        if not self.serial_bus.serial.isOpen():
            logging.debug("COM port in NOT open!")
            return
        self.status.start()
        logging.debug("Initializing...")

        while not self.status.is_initialized:
            sleep(self.command_update_interval)
        logging.debug("Initializing Finished!")
        self.approve()
        self.move(0, 0, 0, 1, 1, 1)
        logging.debug("Config Approved!")
        i = 123
        j = 456
        z = 789
        while not self.done:
            sleep(self.command_update_interval)
            self.move(i, j, z, 1000, 1000, 1000)

