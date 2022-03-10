from socket import timeout
import serial
import serial.tools.list_ports


def enumerate_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))


class Communication:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate=baudrate, bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=0)

    def connect(self):
        self.serial.open()

    def disconnect(self):
        self.serial.close()

    def send(self, data):
        self.serial.write(data)
