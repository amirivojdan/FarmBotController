from threading import Thread
from time import sleep
from CommandGenerator import CommandGenerator
from CommunicationBus import CommunicationBus
from FarmBotStatus import FarmBotStatus


class FarmBot(Thread):
    """High-level python class to wrap all underlying details required to control
    the FarmBot."""

    def __init__(self, port, baud_rate=115200, command_update_frequency=100,
                 status_update_frequency=100, logging_enabled=True):
        Thread.__init__(self)
        self.done = False
        self.serial_bus = CommunicationBus(port, baud_rate)
        self.status = FarmBotStatus(status_update_frequency, self.serial_bus)
        self.command_generator = CommandGenerator()
        self.command_update_interval = 1/command_update_frequency  # T=1/f

    def connect(self):
        print("Connected!")
        self.serial_bus.connect()

    def disconnect(self):
        print("Disconnected!")
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
            print("COM port in NOT open!")
            return
        self.status.start()
        print("Initializing...")
        while not self.status.is_initialized:
            sleep(self.command_update_interval)
        print("Initializing Finished!")
        self.approve()
        print("Config Approved!")
        i=0
        j=0
        while not self.done:
            i+=100
            j-=20
            sleep(5)
            self.move(i, j, 100, 1000, 1000, 1000)

