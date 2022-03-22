from threading import Thread
from time import sleep
from CommunicationBus import CommunicationBus, enumerate_ports
from FarmBotStatus import FarmBotStatus
import logging


class FarmBot(Thread):
    """High-level python class to wrap all underlying details required to control
    the FarmBot."""

    def __init__(self, port=None, baud_rate=115200, command_update_frequency=200,
                 status_update_frequency=200):
        Thread.__init__(self)
        if not port:
            for available_port, desc, hwid in sorted(enumerate_ports()):
                if "Arduino Mega 2560" in desc:
                    if port:
                        logging.error("MORE THAN ONE ARDUINO COM PORT AVAILABLE!!!")
                        raise Exception("More than one Arduino COM port available."
                                        " Please explicitly define COM port "
                                        "in FarmBot constructor!")
                    port = available_port

        self.serial_bus = CommunicationBus(port, baud_rate)
        self.status = FarmBotStatus(status_update_frequency, self.serial_bus)
        self.command_update_interval = 1 / command_update_frequency  # T=1/f
        self.queue_number = ' Q0'

    def approve(self):
        command = 'F22 P2 V1' + self.queue_number
        self.serial_bus.send(command)

    def move_with_speed(self, x, y, z, x_speed, y_speed, z_speed):
        command = 'G00 X{x} Y{y} Z{z} A{x_speed} B{y_speed} C{z_speed}'.format(x=x, y=y, z=z,
                                                                               x_speed=x_speed,
                                                                               y_speed=y_speed,
                                                                               z_speed=z_speed) + self.queue_number
        self.serial_bus.send(command)

    def move(self, x, y, z):
        command = 'G00 X{x} Y{y} Z{z}'.format(x=x, y=y, z=z) + self.queue_number
        self.serial_bus.send(command)

    def move_home_all(self):
        command = 'G28' + self.queue_number
        self.serial_bus.send(command)

    def home_x_axis(self):
        command = 'F11' + self.queue_number
        self.serial_bus.send(command)

    def home_y_axis(self):
        command = 'F12' + self.queue_number
        self.serial_bus.send(command)

    def home_z_axis(self):
        command = 'F13' + self.queue_number
        self.serial_bus.send(command)

    def calibrate_x_axis(self):
        command = 'F14' + self.queue_number
        self.serial_bus.send(command)

    def calibrate_y_axis(self):
        command = 'F15' + self.queue_number
        self.serial_bus.send(command)

    def calibrate_z_axis(self):
        command = 'F16' + self.queue_number
        self.serial_bus.send(command)

    def list_all_parameters(self):
        command = "F20" + self.queue_number
        self.serial_bus.send(command)

    def read_parameter(self, p):
        command = 'F21 P{p}'.format(p=p) + self.queue_number
        self.serial_bus.send(command)

    def write_parameter(self, p, v):
        command = 'F22 P{p} V{v}'.format(p=p, v=v) + self.queue_number
        self.serial_bus.send(command)

    def update_parameter(self, p, v):
        command = 'F23 P{p} V{v}'.format(p=p, v=v) + self.queue_number
        self.serial_bus.send(command)

    def read_status(self, p):
        command = 'F31 P{p}'.format(p=p) + self.queue_number
        self.serial_bus.send(command)

    def write_status(self, p, v):
        command = 'F32 P{p} V{v}'.format(p=p, v=v) + self.queue_number
        self.serial_bus.send(command)

    def set_pin(self, p, v, m):
        command = 'F41 P{p} V{v} M{m}'.format(p=p, v=v, m=m) + self.queue_number
        self.serial_bus.send(command)

    def read_pin(self, p, m):
        command = 'F42 P{p} M{m}'.format(p=p, m=m) + self.queue_number
        self.serial_bus.send(command)

    def set_pin_io_mode(self, p, m):
        command = 'F43 P{p} M{m}'.format(p=p, m=m) + self.queue_number
        self.serial_bus.send(command)

    def set_pin_wait_set_pin(self, p, v, w, t, m):
        command = 'F43 P{p} V{v} W{w} T{t} M{m}'.format(p=p, v=v, w=w, t=t, m=m) + self.queue_number
        self.serial_bus.send(command)

    def set_i2c_value(self, e, p, v):
        command = 'F51 E{e} P{p} V{v}'.format(e=e, p=p, v=v) + self.queue_number
        self.serial_bus.send(command)

    def read_i2c_value(self, e, p):
        command = 'F52 E{e} P{p}'.format(e=e, p=p) + self.queue_number
        self.serial_bus.send(command)

    def set_servo_pin_angle(self, p, v):
        command = 'F61 P{p} V{v}'.format(p=p, v=v) + self.queue_number
        self.serial_bus.send(command)

    def reset_emergency_stop(self):
        command = 'F09' + self.queue_number
        self.serial_bus.send(command)

    def report_end_stop(self):
        command = 'F81' + self.queue_number
        self.serial_bus.send(command)

    def report_current_position(self):
        command = 'F82' + self.queue_number
        self.serial_bus.send(command)

    def report_software_version(self):
        command = 'F83' + self.queue_number
        self.serial_bus.send(command)

    def set_current_position_to_zero(self, x, y, z):
        command = 'F84 X{x} Y{y} Z{z}'.format(x=x, y=y, z=z) + self.queue_number
        self.serial_bus.send(command)

    def emergency_stop(self):
        command = "E" + self.queue_number
        self.serial_bus.send(command)

    def movement_abort(self):
        command = "@" + self.queue_number
        self.serial_bus.send(command)

    def connect(self):
        logging.debug("Connected!")
        self.serial_bus.connect()

    def disconnect(self):
        logging.debug("Disconnected!")
        self.serial_bus.disconnect()

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

        logging.debug("Config Approved!")
        i = 100
        j = 100
        z = 100

        sleep(5)
        self.move(-200, 0, 0)
