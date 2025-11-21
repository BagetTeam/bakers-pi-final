from time import sleep
from color_sensor.color_sensor import ColorSensor
from utils.brick import Motor, wait_ready_sensors
from robot_movement.robot_movement import RobotMovement
from robot_delivery.delivery_system import DeliverySystem

MOTOR_POWER = 30


class ZoneDetection:
    color_sensor: ColorSensor
    delivery: DeliverySystem
    movement: RobotMovement

    def __init__(
        self,
        color_sensor: ColorSensor,
        delivery_system: DeliverySystem,
        movement: RobotMovement,
    ):
        self.color_sensor = color_sensor
        self.delivery = delivery_system
        self.movement = movement

    def detect_zones(self):
        while True:
            color = self.color_sensor.get_current_color()
            sleep(0.1)
            print(color)
            if color == "ORANGE":
                self.movement.move_straight(-MOTOR_POWER)
                sleep(0.5)
                self.movement.corner_turn_left(MOTOR_POWER)
                sleep(0.5)
                # movement.move_straight(MOTOR_POWER)
                # sleep(x)
                self.movement.corner_turn_right(MOTOR_POWER)
                sleep(0.5)
                self.movement.move_straight(MOTOR_POWER)
            elif color == "GREEN":
                self.movement.stop_move()
                sleep(0.3)
                self.movement.change_relative_angle(45, -90)
                sleep(1)
                self.delivery.deliver()
                self.movement.change_relative_angle(-45, 90)
                sleep(1)
                self.movement.move_straight(MOTOR_POWER)

            elif color == "RED":
                self.movement.stop_move()
                sleep(0.3)
                self.movement.change_relative_angle(-500, 500)
                sleep(5)
                self.movement.move_straight(MOTOR_POWER)
