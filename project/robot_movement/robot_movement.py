from time import sleep
from utils.brick import (
    Motor,
)

class RobotMovement:
    def __init__(self, left_motor: Motor, right_motor: Motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

    def move_straight(self, power: int):
        self.left_motor.set_power(power)
        self.right_motor.set_power(power)

    def stop_move(self):
        self.left_motor.set_power(0)
        self.right_motor.set_power(0)

    def intersection_turn_right(self, power: int):
        self.left_motor.set_power(power)
        self.right_motor.set_power(-power)

    def intersection_turn_left(self, power: int):
        self.left_motor.set_power(-power)
        self.right_motor.set_power(power)
    
    def corner_turn_right(self, power: int):
        self.left_motor.set_power(0)
        self.right_motor.set_power(power)

    def corner_turn_left(self, power: int):
        self.left_motor.set_power(power)
        self.right_motor.set_power(0)

    def adjust_speed(self, left_power: int, right_power: int):
        self.left_motor.set_power(left_power)
        self.right_motor.set_power(right_power)

    def change_relative_angle(self, angleLeft: int, angleRight: int):
        self.left_motor.set_position_relative(angleLeft)
        self.right_motor.set_position_relative(angleRight)