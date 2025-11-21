from time import sleep
from color_sensor.color_sensor import ColorSensor
from gyro_sensor.gyro_sensor import GyroSensor
from robot_delivery.delivery_system import DeliverySystem
from robot_movement.robot_movement import RobotMovement


class PackageDiscovery:
    color_sensor: ColorSensor
    robot_movement: RobotMovement
    gyro_sensor: GyroSensor
    delivery_system: DeliverySystem

    def __init__(
        self,
        gyro_sensor: GyroSensor,
        color_sensor: ColorSensor,
        robot_movement: RobotMovement,
        delivery_system: DeliverySystem,
    ):
        self.color_sensor = color_sensor
        self.robot_movement = robot_movement
        self.gyro_sensor = gyro_sensor
        self.delivery_system = delivery_system

    def explore_room(self):
        BASE_L = 20
        BASE_R = 20
        advance_time = 0.5

        package_found = False
        advances = 0
        self.gyro_sensor.set_reference()
        print("GOING WITH REFERENCE:", self.gyro_sensor.get_angle())
        while not package_found and advances < 10:
            advances += 1
            print("Advance:", advances)
            # Check left
            print("Checking LEFT")
            self.robot_movement.adjust_speed(0, BASE_R)
            while self.gyro_sensor.get_angle() > -50:
                if self.color_sensor.get_current_color() == "GREEN":
                    package_found = True
                    print("PACKAGE FOUUND")
                    self.delivery_package()
                    break
                sleep(0.01)
            sleep(0.5)
            print("Turning back LEFT")
            self.robot_movement.adjust_speed(0, -BASE_R)
            while self.gyro_sensor.get_angle() < 0:
                sleep(0.1)

            if package_found:  # early exit
                break

            print("Checking RIGHT")
            # Check right
            self.robot_movement.adjust_speed(BASE_L, 0)
            while self.gyro_sensor.get_angle() < 50:
                if self.color_sensor.get_current_color() == "GREEN":
                    package_found = True
                    print("PACKAGE FOUUND")
                    self.delivery_package()
                    break
                sleep(0.01)
            sleep(0.5)
            print("Turning back RIGHT")
            self.robot_movement.adjust_speed(-BASE_L, 0)
            while self.gyro_sensor.get_angle() > 0:
                sleep(0.1)

            # Advance
            self.robot_movement.adjust_speed(BASE_L, BASE_R)
            sleep(advance_time)
            self.robot_movement.adjust_speed(0, 0)

        self.robot_movement.adjust_speed(-BASE_L, -BASE_R)
        sleep(advance_time * advances)
        self.robot_movement.adjust_speed(0, 0)

    def delivery_package(self):
        self.robot_movement.adjust_speed(0, 0)
        sleep(0.2)
        self.robot_movement.adjust_speed(-10, -10)
        sleep(0.3)
        self.robot_movement.adjust_speed(0, 0)
        sleep(1)
        self.delivery_system.deliver()
        sleep(1)
        self.robot_movement.adjust_speed(10, 10)
        sleep(0.3)
        self.robot_movement.adjust_speed(0, 0)
        sleep(0.2)

