class FarmBotStatus:
    """Receives the packets from the FarmBot and interpret them according to
     the table provided by the manufacturer in
     https://github.com/farmbot/farmbot-arduino-firmware#codes-received-from-the-arduino """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
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
            }

    def print(self):
        pass

    def interpret(self, raw_response: str):
        response_chunks = raw_response.split()
        if response_chunks and (response_chunks[0] in self.reports_mapping):
            print(self.reports_mapping[response_chunks[0]])

    def update(self, raw_response: str):
        self.interpret(raw_response)
        if raw_response.startswith("R00"):
            self.is_idle = True
            if self.is_idle and not self.is_initialized:
                self.is_initialized = True

        if raw_response.startswith("R01"):
            self.command_started = True
            self.command_completed = False

        if raw_response.startswith("R02"):
            self.command_started = False
            self.command_completed = True

        if raw_response.startswith("R09"):
            self.invalid_command = True

        if raw_response.startswith("R71"):
            self.x_axis_timeout = True

        if raw_response.startswith("R72"):
            self.y_axis_timeout = True

        if raw_response.startswith("R73"):
            self.z_axis_timeout = True

        if raw_response.startswith("R87"):
            self.emergency_lock = True

        if raw_response.startswith("R88"):
            self.no_config = True