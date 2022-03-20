class CommandGenerator:
    """Simply generates G-Codes based on the instructions' table provided by
     the manufacturer in
    https://github.com/farmbot/farmbot-arduino-firmware#codes-sent-to-the-arduino """

    def __init__(self, queue_number: str = 'Q0'):
        self.queue_number = ' ' + queue_number

    def approve(self):
        return 'F22 P2 V1' + self.queue_number

    def move(self, x, y, z, x_speed, y_speed, z_speed):
        return 'G00 X{x} Y{y} Z{z} A{x_speed} B{y_speed} C{z_speed}'.format(x=x, y=y, z=z,
                                                                            x_speed=x_speed,
                                                                            y_speed=y_speed,
                                                                            z_speed=z_speed) + self.queue_number

    def move_home_all(self):
        return 'G28' + self.queue_number

    def home_x_axis(self):
        return 'F11' + self.queue_number

    def home_y_axis(self):
        return 'F12' + self.queue_number

    def home_z_axis(self):
        return 'F13' + self.queue_number

    def calibrate_x_axis(self):
        return 'F14' + self.queue_number

    def calibrate_y_axis(self):
        return 'F15' + self.queue_number

    def calibrate_z_axis(self):
        return 'F16' + self.queue_number

    def list_all_parameters(self):
        return "F20" + self.queue_number

    def read_parameter(self, p):
        return 'F21 P{p}'.format(p=p) + self.queue_number

    def write_parameter(self, p, v):
        return 'F22 P{p} V{v}'.format(p=p, v=v) + self.queue_number

    def update_parameter(self, p, v):
        return 'F23 P{p} V{v}'.format(p=p, v=v) + self.queue_number

    def read_status(self, p):
        return 'F31 P{p}'.format(p=p) + self.queue_number

    def write_status(self, p, v):
        return 'F32 P{p} V{v}'.format(p=p, v=v) + self.queue_number

    def set_pin(self, p, v, m):
        return 'F41 P{p} V{v} M{m}'.format(p=p, v=v, m=m) + self.queue_number

    def read_pin(self, p, m):
        return 'F42 P{p} M{m}'.format(p=p, m=m) + self.queue_number

    def set_pin_io_mode(self, p, m):
        return 'F43 P{p} M{m}'.format(p=p, m=m) + self.queue_number

    def set_pin_wait_set_pin(self, p, v, w, t, m):
        return 'F43 P{p} V{v} W{w} T{t} M{m}'.format(p=p, v=v, w=w, t=t, m=m) + self.queue_number

    def set_i2c_value(self, e, p, v):
        return 'F51 E{e} P{p} V{v}'.format(e=e, p=p, v=v) + self.queue_number

    def read_i2c_value(self, e, p):
        return 'F52 E{e} P{p}'.format(e=e, p=p) + self.queue_number

    def set_servo_pin_angle(self, p, v):
        return 'F61 P{p} V{v}'.format(p=p, v=v) + self.queue_number

    def reset_emergency_stop(self):
        return 'F09' + self.queue_number

    def report_end_stop(self):
        return 'F81' + self.queue_number

    def report_current_position(self):
        return 'F82' + self.queue_number

    def report_software_version(self):
        return 'F83' + self.queue_number

    def set_current_position_to_zero(self, x, y, z):
        return 'F84 X{x} Y{y} Z{z}'.format(x=x, y=y, z=z) + self.queue_number

    def emergency_stop(self):
        return "E" + self.queue_number

    def movement_abort(self):
        return "@" + self.queue_number
