import math

import pygame
from pygame.joystick import Joystick


class Extreme3dPro:

    def __init__(self, joystick_id=0):
        pygame.init()
        pygame.joystick.init()
        self.controller = Joystick(joystick_id)
        print("Connected Joystick Model:{model}".format(model=self.controller.get_name()))
        self.number_of_axis = self.controller.get_numaxes()
        self.number_of_buttons = self.controller.get_numbuttons()
        self.boundary_tolerance = 0.09
        self.decimal_points = 2

        self.pitch_axis_index = 1
        self.roll_axis_index = 0
        self.yaw_axis_index = 2

        self.pitch_axis_dir = -1
        self.roll_axis_dir = 1
        self.yaw_axis_dir = 1

        self.pitch = 0
        self.roll = 0
        self.yaw = 0

        self.max_max_value = 1

    def remove_boundary_tolerance(self, value, max_value):
        if abs(value) < self.boundary_tolerance:
            return 0
        if max_value-abs(value) < self.boundary_tolerance:
            return math.copysign(max_value, value)
        return value

    def update(self):
        pygame.event.pump()
        # i=1 => -y axis(pitch)
        # i=0 => x axis(roll)
        # i=2 => z axis(yaw)
        pitch_value = round(self.controller.get_axis(self.pitch_axis_index), self.decimal_points)
        roll_value = round(self.controller.get_axis(self.roll_axis_index), self.decimal_points)
        yaw_value = round(self.controller.get_axis(self.yaw_axis_index), self.decimal_points)

        self.pitch = self.remove_boundary_tolerance(pitch_value, self.max_max_value) * self.pitch_axis_dir
        self.roll = self.remove_boundary_tolerance(roll_value, self.max_max_value) * self.roll_axis_dir
        self.yaw = self.remove_boundary_tolerance(yaw_value, self.max_max_value) * self.yaw_axis_dir
