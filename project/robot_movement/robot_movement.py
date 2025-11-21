from time import sleep
from utils.brick import (
    Motor,
)


class RobotMovement:
    left_motor: Motor
    right_motor: Motor

    def __init__(self, left_motor: Motor, right_motor: Motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.right_motor.reset_encoder()
        self.right_motor.set_limits(50)
        self.left_motor.reset_encoder()
        self.left_motor.set_limits(50)
        sleep(1)

    def set_limits(self, power: int = 0, dps: int = 0):
        self.left_motor.set_limits(power, dps)
        self.right_motor.set_limits(power, dps)

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

    def adjust_left_speed(self, left_power: int):
        self.left_motor.set_power(left_power)

    def adjust_speed(self, left_power: int, right_power: int):
        self.left_motor.set_power(left_power)
        self.right_motor.set_power(right_power)

    def change_relative_angle(self, angleLeft: int, angleRight: int):
        if angleLeft != 0:
            self.left_motor.set_position_relative(angleLeft)
        if angleRight != 0:
            self.right_motor.set_position_relative(angleRight)

    def is_robot_motor_moving(self) -> bool:
        return (self.left_motor.is_moving() or False) or (
            self.right_motor.is_moving() or False
        )
