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

    def intersection_turn_right(self):
        self.gyro_sensor.set_reference()
        self.adjust_speed(30, -5)
        while self.gyro_sensor.get_angle() < 90:
            sleep(0.01)
        self.adjust_speed(0, 0)

    def intersection_turn_left(self):
        self.gyro_sensor.set_reference()
        self.adjust_speed(-5, 30)
        while self.gyro_sensor.get_angle() > -90:
            sleep(0.01)
        self.adjust_speed(0, 0)

    def adjust_left_speed(self, left_power: float):
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
