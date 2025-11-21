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
    has_found: bool = False

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
            if self.enabled:
                color = self.color_sensor.get_current_color()

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

            sleep(0.1)

    def detect_zone(self):
        color = self.color_sensor.get_current_color()

        if color == "ORANGE":
            print("ORANGE")
            self.discover_color()

    def discover_color(self):
        t = Thread(target=self.__move_around)
        t.start()

        while not self.has_found:
            color = self.color_sensor.get_current_color()
            if color == "RED":
                self.has_found = True
                self.__backtrack()

            sleep(0.01)

        t.join()

    def __backtrack(self):
        self.movement.change_relative_angle(-50, -50)
        sleep(2)

    def __move_around(self):
        self.movement.change_relative_angle(50, 50)
        sleep(2)

        if self.has_found:
            self.movement.change_relative_angle(-50, -50)
            sleep(2)
            return

        self.movement.change_relative_angle(50, -50)
        sleep(2)

        if self.has_found:
            self.movement.change_relative_angle(-50, 50)
            sleep(2)
            return

        self.movement.change_relative_angle(-100, 100)
        sleep(2)

        if self.has_found:
            self.movement.change_relative_angle(50, -50)
            return
