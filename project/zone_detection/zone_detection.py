from threading import Thread
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
    enabled: bool = False
    has_found_red: bool = False

    def __init__(
        self,
        color_sensor: ColorSensor,
        delivery_system: DeliverySystem,
        movement: RobotMovement,
    ):
        self.color_sensor = color_sensor
        self.delivery = delivery_system
        self.movement = movement

    def detect_zone(self):
        color = self.color_sensor.get_current_color()

        if color == "ORANGE":
            print("ORANGE")
            self.discover_color()

    def discover_color(self):
        t = Thread(target=self.__move_around)
        t.start()

        while not self.has_found_red:
            color = self.color_sensor.get_current_color()
            if color == "RED":
                self.has_found_red = True
                print("FOUND RED")

            sleep(0.01)

        t.join()

    def __backtrack(self):
        self.movement.set_limits(20)
        sleep(0.5)
        self.movement.change_relative_angle(-50, -50)
        sleep(1)
        self.movement.set_limits(0)
        sleep(1)

        self.movement.turn_with_angle(-180, 30)

    def __move_around(self):
        self.movement.set_limits(20)
        sleep(0.5)
        self.movement.change_relative_angle(0, 90)
        sleep(1)
        self.movement.change_relative_angle(90, 0)
        sleep(1)

        if self.has_found_red:
            self.__backtrack()
            return

        self.movement.turn_with_angle(-30)
        sleep(0.5)

        if self.has_found_red:
            self.movement.turn_with_angle(-self.movement.gyro_sensor.get_angle())
            self.__backtrack()
            return

        self.movement.turn_with_angle(60)
        self.movement.turn_with_angle(-self.movement.gyro_sensor.get_angle())

        if self.has_found_red:
            self.__backtrack()
