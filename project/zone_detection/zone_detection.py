from threading import Thread
from time import sleep
from color_sensor.color_sensor import ColorSensor
from utils.brick import Motor, wait_ready_sensors
from robot_movement.robot_movement import RobotMovement
from robot_delivery.delivery_system import DeliverySystem
from package_discovery.package_discovery import PackageDiscovery

MOTOR_POWER = 30


class ZoneDetection:
    color_sensor: ColorSensor
    delivery: DeliverySystem
    movement: RobotMovement
    enabled: bool = False
    has_found_red: bool = False
    stop: bool = False
    package_discorvery: PackageDiscovery
    run_thread: bool = True
    is_discovering: bool = False

    def __init__(
        self,
        color_sensor: ColorSensor,
        delivery_system: DeliverySystem,
        movement: RobotMovement,
        package_discovery: PackageDiscovery,
    ):
        self.color_sensor = color_sensor
        self.delivery = delivery_system
        self.movement = movement
        self.package_discorvery = package_discovery

    def detect_zone(self):
        self.movement.adjust_speed(0, 0)
        has_found = self.discover_color()
        self.enabled = False
        return has_found

    def discover_color(self):
        print("discovering")
        self.is_discovering = True

        self.has_found_red = False
        self.stop = False
        # t = Thread(target=self.__move_around)
        # t.start()
        #
        # while not self.stop:
        #     color = self.color_sensor.get_current_color()
        #     if color == "RED":
        #         self.has_found_red = True
        #         self.stop = True
        #         print("FOUND RED")
        #
        #     sleep(0.01)
        #
        # t.join()

        package_found = False
        if not self.has_found_red:
            package_found = self.package_discorvery.explore_room()

        self.__backtrack()
        self.is_discovering = False
        return package_found

    def __backtrack(self):
        sleep(0.5)

        self.movement.turn_specific_with_angle(178, -20, 30)

    def __move_around(self):
        self.movement.a_bit_forward()

        self.stop = True
