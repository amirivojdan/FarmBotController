import logging
from threading import Thread
from time import sleep

from CommunicationBus import CommunicationBus


class FarmBotStatus(Thread):
    """Receives the packets from the FarmBot and interpret them according to
     the table provided by the manufacturer in
     https://github.com/farmbot/farmbot-arduino-firmware#codes-received-from-the-arduino """

    def __init__(self, reading_frequency, serial_bus: CommunicationBus):
        Thread.__init__(self)
        self.done = False
        self.reading_update_interval = 1 / reading_frequency  # T=1/f
        self.serial_bus = serial_bus

        self.x = 0
        self.y = 0
        self.z = 0

        self.x_encoder_raw = 0
        self.y_encoder_raw = 0
        self.z_encoder_raw = 0

        self.x_encoder_scaled = 0
        self.y_encoder_scaled = 0
        self.z_encoder_scaled = 0

        self.logging_enabled = False
        self.is_idle = False
        self.is_initialized = False
        self.emergency_lock = False
        self.invalid_command = False
        self.no_config = False
        self.x_axis_timeout = False
        self.y_axis_timeout = False
        self.z_axis_timeout = False

        self.command_started = False
        self.command_completed = False

        self.reports_mapping = {
            "R00": "Idle",
            "R01": "Current command started",
            "R02": "Current command finished successfully",
            "R03": ("V", "Current command finished with error"),
            "R04": "Current command running",
            "R05": ("X Y Z", "Report motor/axis state"),
            "R06": ("X Y Z", "Report calibration state during execution"),
            "R07": "Retry movement",
            "R08": "Command echo",
            "R09": "Command invalid",
            "R11": "X axis homing complete",
            "R12": "Y axis homing complete",
            "R13": "Z axis homing complete",
            "R15": ("X", "Firmware used a different X coordinate than given in move command"),
            "R16": ("Y", "Firmware used a different Y coordinate than given in move command"),
            "R17": ("Z", "Firmware used a different Z coordinate than given in move command"),
            "R20": "Report all parameters complete",
            "R21": ("P V", "Report parameter value"),
            "R23": ("P V", "Report updated parameter (during calibration)"),
            "R31": ("P V", "Report status value (not enabled)"),
            "R41": ("P V", "Report pin value"),
            "R61": ("P V", "Report pin monitor analog value"),
            "R71": "X axis timeout",
            "R72": "Y axis timeout",
            "R73": "Z axis timeout",
            "R81": ("XA XB YA YB ZA ZB", "Report end stops"),
            "R82": ("X Y Z", "Report current position"),
            "R83": "Report software version",
            "R84": ("X Y Z", "Report encoder position scaled"),
            "R85": ("X Y Z", "Report encoder position raw"),
            "R86": "Report movement abort",
            "R87": "Emergency lock",
            "R88": "No config",
            "R89": ("U X V Y W Z", "Report # axis steps (U,V,W) and highest missed steps in last 500 (X,Y,Z)"),
            "R99": "Debug message"
        }

    def print(self):
        pass

    def interpret(self, response_chunks: list[str]):
        params = {}
        if response_chunks and (response_chunks[0] in self.reports_mapping):
            for i in range(1, len(response_chunks) - 1):
                parameter_value = ''.join(j for j in response_chunks[i] if (j.isdigit() or j == '.' or j == '-'))
                if parameter_value:
                    parameter_key = ''.join(j for j in response_chunks[i] if (j.isalpha() and j != '-'))
                    params[parameter_key] = float(parameter_value)
            return params
        return None

    def update_internal_variables(self, response_chunks: list[str], parameters: dict):
        # R00 is the idle status, R00 first seen considered as the initialized state
        if response_chunks and (response_chunks[0] in self.reports_mapping):
            if "R00" in response_chunks[0] and not self.is_initialized:
                self.is_initialized = True

            if "R82" in response_chunks[0] and len(parameters) == 3:
                self.x = parameters["X"]
                self.y = parameters["Y"]
                self.z = parameters["Z"]

            if "R84" in response_chunks[0] and len(parameters) == 3:
                self.x_encoder_scaled = parameters["X"]
                self.y_encoder_scaled = parameters["Y"]
                self.z_encoder_scaled = parameters["Z"]

            if "R85" in response_chunks[0] and len(parameters) == 3:
                self.x_encoder_raw = parameters["X"]
                self.y_encoder_raw = parameters["Y"]
                self.z_encoder_raw = parameters["Z"]

    def update_status(self):
        raw_responses = self.serial_bus.fetch_responses()
        if raw_responses is not None:
            for raw_response in raw_responses:

                logging.debug(raw_response)
                response_chunks = raw_response.split()
                parameters = self.interpret(response_chunks)
                self.update_internal_variables(response_chunks, parameters)
                if parameters:
                    for key in parameters:
                        logging.info("{key}={value}".format(key=key, value=parameters[key]))

    def run(self):
        if not self.serial_bus.serial.isOpen():
            logging.debug("COM port in NOT open!")
            return

        while not self.done:
            self.update_status()
            sleep(self.reading_update_interval)
