import serial
import serial.tools.list_ports


def enumerate_ports():
    """Enumerate through all the available COM ports
     (to be used in the start menu & automatic connection)"""
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))


class CommunicationBus:
    def __init__(self, port, baudrate=115200):
        """Initializing the serial port object without opening the port!"""
        self.serial = serial.Serial()  # it will not instantly open the serial port
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.parity = serial.PARITY_NONE
        self.serial.timeout = 0
        self.encoding = 'ASCII'
        self.crlf = '\r\n'

    def connect(self):
        self.serial.open()

    def disconnect(self):
        self.serial.close()

    def send(self, data: str):
        self.serial.write((data+self.crlf).encode(self.encoding))

    def fetch_responses(self):
        decoded_responses = []
        if self.serial.inWaiting():
            raw_responses = self.serial.readlines()
            for item in raw_responses:
                decoded_responses.append(item.decode(self.encoding))
            return decoded_responses
        return None
