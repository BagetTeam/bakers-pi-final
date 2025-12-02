from time import sleep
from gyro_sensor.gyro_sensor import GyroSensor
from utils.brick import (
    Motor,
)


class RobotMovement:
    left_motor: Motor
    right_motor: Motor
    gyro_sensor: GyroSensor

    BASE_R_POWER: int = 20
    BASE_L_POWER: int = 10

    def __init__(self, left_motor: Motor, right_motor: Motor, gyro_sensor: GyroSensor):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro_sensor = gyro_sensor

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

    def intersection_turn_right(self, deg: int):
        self.gyro_sensor.set_reference()
        self.adjust_speed(30, -8)
        while self.gyro_sensor.get_angle() < deg:
            sleep(0.01)
        self.adjust_speed(0, 0)

    def turn_with_angle(self, angle: float, base_power: float = 10):
        isRight = 1 if angle > 0 else -1
        self.gyro_sensor.set_reference()
        self.adjust_speed(isRight * base_power, -isRight * base_power)

        while abs(self.gyro_sensor.get_angle()) < abs(angle):
            sleep(0.01)
        self.adjust_speed(0, 0)

    def turn_specific_with_angle(
        self, angle: float, left_power: float = 10, right_power: float = 10
    ):
        self.gyro_sensor.set_reference()
        self.adjust_speed(left_power, right_power)

        while abs(self.gyro_sensor.get_angle()) < abs(angle):
            sleep(0.01)
        self.adjust_speed(0, 0)

    def turn_specific_with_angle_without_refs(
        self, angle: float, left_power: float = 10, right_power: float = 10
    ):
        self.adjust_speed(left_power, right_power)

        while abs(self.gyro_sensor.get_angle()) < abs(angle):
            sleep(0.01)
        self.adjust_speed(0, 0)

    def adjust_left_speed(self, left_power: float):
        self.left_motor.set_power(left_power)

    def adjust_speed(self, left_power: float, right_power: float):
        self.left_motor.set_power(left_power)
        self.right_motor.set_power(right_power)

    def change_relative_angle(self, angleLeft: float, angleRight: float):
        if angleLeft != 0:
            self.left_motor.set_position_relative(angleLeft)
        if angleRight != 0:
            self.right_motor.set_position_relative(angleRight)

    def is_robot_motor_moving(self) -> bool:
        return (self.left_motor.is_moving() or False) or (
            self.right_motor.is_moving() or False
        )

    def a_bit_forward(self):
        self.turn_specific_with_angle(30, -20, 20)
        sleep(0.1)
        self.turn_specific_with_angle(30, 20, 10)
        sleep(0.1)
